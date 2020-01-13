from datahub import DataHub


access_id = 'NE5RYcFUSOkzSUQK'
access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'

endpoint = 'http://15.74.19.36'

project_name = 'city_brain'
topic_name = 'dwd_tfc_opt_lane_queue_radar_rt_chongming'

dh = DataHub(access_id, access_key, endpoint)

shard_result = dh.list_shard(project_name, topic_name)
shards = shard_result.shards
print(len(shards))