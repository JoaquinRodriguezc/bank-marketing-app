"""V2 revisada desde E2: variables determinísticas y búsqueda train-only."""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import f1_score, average_precision_score, precision_score, recall_score
from transformadores import DerivarColumnas, COLUMNAS_ENTRADA

MODOS=['original','desconocidos','saldo_log','saldo_deudas','sin_contacto','combinado','e2_exacto','e2_deudas']
UMBRALES=np.array([0.,.02,.05,.075,.1,.15,.2,.3,.4,.5,.6,.7])

def signlog(x):return np.sign(x)*np.log1p(np.abs(x))

class VariablesE2(BaseEstimator, TransformerMixin):
    def __init__(self,modo='original'):self.modo=modo
    def fit(self,X,y=None):
        if self.modo not in MODOS:raise ValueError(self.modo)
        return self
    def transform(self,X):
        # Lista cerrada, sin copiar identificador, duration, fecha ni objetivo.
        if self.modo.startswith('e2_'):
            z=X[['age','job','education','housing','loan']].copy()
            z['balance_signed_log']=signlog(X.balance)
            z['previous_log']=np.log1p(X.previous)
            z['tiene_historial']=X.pdays.ne(-1).astype(int)
            z['dias_desde_contacto']=X.pdays.where(X.pdays.ne(-1),np.nan).astype(float)
            z['poutcome_limpio']=X.poutcome.fillna(pd.Series(np.where(X.pdays.eq(-1),'sin_historial','desconocido_con_historial'),index=X.index))
            for c in ['job','education']:z[c]=z[c].fillna('desconocido')
        else:
            z=DerivarColumnas(usar_campaign=False,usar_dia=False,job_como='estudiante_o_jubilado').transform(X[COLUMNAS_ENTRADA])
            if self.modo in ['desconocidos','combinado']:
                # job ya está agrupada: conservar por separado el desconocimiento de ocupación.
                z['job_desconocido']=X.job.isna().astype(int)
                z['education']=X.education.fillna('desconocido')
                z['poutcome']=X.poutcome.fillna(pd.Series(np.where(X.pdays.eq(-1),'nunca_contactado','desconocido_con_historial'),index=X.index))
            if self.modo in ['saldo_log','saldo_deudas','combinado']:
                z['balance_signed_log']=signlog(X.balance)
                z=z.drop(columns='balance')
            if self.modo in ['sin_contacto','combinado']:z=z.drop(columns='contact_type')
        if self.modo in ['saldo_deudas','combinado','e2_deudas']:
            z['saldo_por_hipoteca']=z.balance_signed_log*X.housing.eq('yes').astype(int)
            z['saldo_por_prestamo']=z.balance_signed_log*X.loan.eq('yes').astype(int)
        return z

def construir(c):
    f=c.get('familia','logistica');peso=c.get('peso','balanced')
    if f=='logistica':m=LogisticRegression(C=c.get('C',1.),class_weight=peso,max_iter=3000,random_state=42)
    elif f=='arbol':m=DecisionTreeClassifier(max_depth=5,min_samples_leaf=100,class_weight='balanced',random_state=42)
    elif f=='bosque':m=RandomForestClassifier(n_estimators=150,max_depth=10,min_samples_leaf=50,class_weight='balanced',random_state=42,n_jobs=1)
    elif f=='boosting':m=HistGradientBoostingClassifier(max_iter=150,learning_rate=.05,max_leaf_nodes=7,min_samples_leaf=100,l2_regularization=10,class_weight='balanced',early_stopping=False,random_state=42)
    else:raise ValueError(f)
    prep=ColumnTransformer([
      ('num',Pipeline([('imputar',SimpleImputer(strategy='median',add_indicator=True)),('escalar',StandardScaler())]),make_column_selector(dtype_include=np.number)),
      ('cat',Pipeline([('imputar',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),make_column_selector(dtype_exclude=np.number))])
    return Pipeline([('derivar',VariablesE2(c['modo'])),('preparar',prep),('modelo',m)])

def configuraciones():
    # Ablaciones con idéntico C y pesos; grilla adicional focalizada en las hipótesis E2.
    cs=[dict(familia='logistica',modo=m,C=1.,peso='balanced') for m in MODOS]
    for modo in ['e2_exacto','e2_deudas']:
        for C in [.1,1.,10.]:
            for peso in [None,'balanced']:
                c=dict(familia='logistica',modo=modo,C=C,peso=peso)
                if c not in cs:cs.append(c)
    cs += [dict(familia=f,modo='e2_deudas',peso='balanced') for f in ['arbol','bosque','boosting']]
    return cs

def medir(c,X,y,splits):
    filas=[]
    for fold,(tr,va) in enumerate(splits,1):
        p=construir(c).fit(X.iloc[tr],y.iloc[tr]).predict_proba(X.iloc[va])[:,1]
        for t in UMBRALES:
            pred=p>=t;real=y.iloc[va]
            filas.append(dict(fold=fold,umbral=t,f1=f1_score(real,pred,zero_division=0),ap=average_precision_score(real,p),
                 precision=precision_score(real,pred,zero_division=0),recall=recall_score(real,pred,zero_division=0)))
    return pd.DataFrame(filas)

def buscar(X,y,splits,configs):
    registros=[];detalles=[]
    for i,c in enumerate(configs):
        d=medir(c,X,y,splits);d.insert(0,'candidato',i);detalles.append(d)
        for t,g in d.groupby('umbral',sort=False):
            registros.append(dict(candidato=i,config=str(c),familia=c['familia'],modo=c['modo'],
                C=c.get('C',np.nan),peso='ninguno' if c.get('peso') is None else c['peso'],umbral=t,
                f1_media=g.f1.mean(),f1_desvio=g.f1.std(ddof=0),ap_media=g.ap.mean(),ap_desvio=g.ap.std(ddof=0),
                precision_media=g.precision.mean(),recall_media=g.recall.mean()))
    tabla=pd.DataFrame(registros).sort_values(['f1_media','ap_media'],ascending=False,kind='stable').reset_index(drop=True)
    return tabla,pd.concat(detalles,ignore_index=True)

def elegir(tabla):
    simple=tabla[tabla.familia.eq('logistica')].iloc[0];mejor=tabla.iloc[0]
    return simple if mejor.familia!='logistica' and mejor.f1_media-simple.f1_media<=simple.f1_desvio else mejor

def anidada(X,y,splits,configs):
    filas=[];internas=[]
    for fold,(tr,va) in enumerate(splits,1):
        xx=X.iloc[tr];yy=y.iloc[tr]
        tabla,_=buscar(xx,yy,list(TimeSeriesSplit(n_splits=3).split(xx)),configs)
        seleccionado=elegir(tabla);tabla.insert(0,'fold_externo',fold);internas.append(tabla)
        c=configs[int(seleccionado.candidato)];t=seleccionado.umbral
        p=construir(c).fit(xx,yy).predict_proba(X.iloc[va])[:,1];pred=p>=t;real=y.iloc[va]
        filas.append(dict(fold=fold,config=str(c),umbral=t,f1=f1_score(real,pred,zero_division=0),
            ap=average_precision_score(real,p),precision=precision_score(real,pred,zero_division=0),recall=recall_score(real,pred,zero_division=0)))
        print('Fold externo',fold,'F1',round(filas[-1]['f1'],5),flush=True)
    return pd.DataFrame(filas),pd.concat(internas,ignore_index=True)
