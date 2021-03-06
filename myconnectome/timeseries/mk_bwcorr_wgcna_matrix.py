"""
make matrix showing bwcorr and wgcna relations
"""

from myconnectome.utils.load_dataframe import load_dataframe
import numpy
import os

basedir=os.environ['MYCONNECTOME_DIR']
df=load_dataframe(os.path.join(basedir,'timeseries/out.dat.wgcna_bwcorr.txt'),0.1)

genemodules=[]
genenums=[]
connections=[]

for k in df.iterkeys():
    genemodules.append(k[0])
    genenums.append(int(k[0].split(':')[0].replace('ME','')))
    c=k[1].replace('Cingulo-opercular','Cingulo_opercular').replace('Parieto-Occipital','Parieto_Occipital').replace('rontal-Parietal','rontal_Parietal')
    connections.append(c)
    

modules=[]
for c in connections:
    c_s=c.split('-')
    assert len(c_s)==2
    modules+=c_s
    
modules=list(set(modules))
modules.sort()
modules=modules[4:]+modules[:4]

modulenums={}
for m in range(len(modules)):
    modulenums[modules[m]]=m
    
connection_nums=numpy.zeros((len(connections),2))
connection_mtx=numpy.zeros((len(modules),len(modules)))
for c in range(len(connections)):
    c_s=connections[c].split('-')
    connection_nums[c,0]=modulenums[c_s[0]]
    connection_nums[c,1]=modulenums[c_s[1]]
    connection_mtx[connection_nums[c,0],connection_nums[c,1]]+=1
    
connection_mtx=connection_mtx + connection_mtx.T
connection_mtx[numpy.tril_indices(connection_mtx.shape[0])]=0
numpy.savetxt(os.path.join(basedir,'timeseries/bwcorr_wgcna_matrix.txt'),connection_mtx)

f=open(os.path.join(basedir,'timeseries/bwcorr_wgcna_netnames.txt'),'w')
for i in modules:
    f.write(i+'\n')
f.close()

f=open(os.path.join(basedir,'rna-seq/WGCNA/module_descriptions.txt'))
mod_desc=[i.strip().split('\t')[1] for i in f.readlines()]
f.close()

h=numpy.histogram(genenums,numpy.arange(0.5,numpy.max(genenums)+1.5,1))
idx=numpy.argsort(h[0])[::-1]
for j in range(len(h[0])):
    i=idx[j]
    if h[0][i]>0:
        print i+1,mod_desc[i],h[0][i]
        


