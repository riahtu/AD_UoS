#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This contains different function defintions for anomaly detection on REFIT
Created on Tue Jan  2 08:54:04 2018

@author: haroonr
"""

def perform_clustering(samp,clusters):
  #TODO: this has not been completed yet
  # http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
  kmeans = KMeans(n_clusters=clusters, random_state=0).fit(samp)
  #kmeans.labels_
  #kmeans.cluster_centers_
  return (kmeans)

def re_organize_clusterlabels(samp):
  """this function checks if labels assigned to data are correct. Less consumption should get lower label and higher should get high label. Doing This maintains consistency across different days and datasets and allows comparison
 input: samp pandas dataframe has  columns: power and cluster
 ouput: pandas dataframe """
  dic = {}
  for i in np.unique(samp.cluster):
    dic[i] = samp[samp.cluster==i].power.iloc[0]
  if not sorted(list(dic.values())) == list(dic.values()):
    #if cluster labels are not assigned acc. to usage levels, i.e., less consumption should get lower label and so on
     p = pd.DataFrame(list(dic.items()))
     p.columns = ['old_label','value']
     q = p.sort_values('value')
     q['new_label'] = range(0,q.shape[0])
     r = dict(zip(q.old_label,q.new_label))
     samp['new_cluster'] =  [r[i] for i in samp['cluster'].values]
     samp.cluster = samp.new_cluster
     samp.drop('new_cluster',axis=1,inplace=True)
  return (samp)

def create_training_stats(traindata):
  """ this method computes cycle frequences and durations from the training data
  Input: pandas series of power data in the python groupby object
  Output: Stats computed in form of dictionary """
  dic = {}
  for k, v in traindata:
    #print(k)
    samp = v.to_frame()
    # handle nans in data
    nan_obs = int(samp.isnull().sum())
    #rule: if more than 50% are nan then I drop that day from calculcations othewise I drop nan readings only
    if nan_obs:  
      if nan_obs >= 0.50*samp.shape[0]:
        print("More than 50percent obs missing hence drop day {} ".format(k))
        #continue
      elif nan_obs < 0.50*samp.shape[0]:
        print("dropping  {} nan observations for day {}".format(nan_obs,k))
        samp.dropna(inplace=True)
    samp.columns = ['power']
    samp_val =  samp.values
    samp_val = samp_val.reshape(-1,1)
    #FIXME: you can play with clustering options
    kobj = perform_clustering(samp_val,clusters=2)
    samp['cluster'] = kobj.labels_
    samp = re_organize_clusterlabels(samp)
    tempval = [(k,sum(1 for i in g)) for k,g in groupby(samp.cluster.values)]
    tempval = pd.DataFrame(tempval,columns=['cluster','samples'])
    off_cycles =list(tempval[tempval.cluster==0].samples)
    on_cycles =list(tempval[tempval.cluster==1].samples)
    temp_dic = {}
    temp_dic["on"] = on_cycles
    temp_dic["off"] = off_cycles
    cycle_stat = Counter(tempval.cluster)
    temp_dic.update(cycle_stat)
    dic[str(k)] = temp_dic
    #% Merge  OFF and ON states of different days into singe lists 
  ON_duration = []
  OFF_duration = []
  ON_cycles = []
  OFF_cycles = []
  for k,v in dic.items():
    ON_duration.append(v['on'])
    OFF_duration.append(v['off'])
    ON_cycles.append(v[1])
    OFF_cycles.append(v[0])
  ON_duration  =  [ item for sublist in ON_duration for item in sublist]
  OFF_duration = [ item for sublist in OFF_duration for item in sublist]
 #%
  summ_dic = {}
  summ_dic['ON_duration'] = {'mean':round(np.mean(ON_duration),3), 'std':round(np.std(ON_duration),3)}
  summ_dic['OFF_duration'] = {'mean':round(np.mean(OFF_duration),3), 'std':round(np.std(OFF_duration),3)}
  summ_dic['ON_cycles'] = {'mean':round(np.mean(ON_cycles),0), 'std':round(np.std(ON_cycles),3)}
  summ_dic['OFF_cycles'] = {'mean':round(np.mean(OFF_cycles),0), 'std':round(np.std(OFF_cycles),3)}
  return (summ_dic)