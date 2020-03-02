from datahub import DataHub


access_id = 'NE5RYcFUSOkzSUQK'
access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'

endpoint = 'http://15.74.19.36'

project_name = 'city_brain'
topic_name = 'ods_devc_signal_info_gb1049_fengxian'

dh = DataHub(access_id, access_key, endpoint)

shard_result = dh.list_shard(project_name, topic_name)
shards = shard_result.shards
shard_num = len(shards)

print(shard_num)




