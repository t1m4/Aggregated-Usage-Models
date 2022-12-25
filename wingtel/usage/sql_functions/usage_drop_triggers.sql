DROP PROCEDURE IF EXISTS create_aggregated_object;
DROP PROCEDURE IF EXISTS update_aggregated_object;
-- INSERT TRIGGER 
DROP TRIGGER IF EXISTS aggregate_data_insert ON usage_datausagerecord;
DROP TRIGGER IF EXISTS aggregate_voice_insert ON usage_voiceusagerecord;
DROP FUNCTION IF EXISTS aggregate_object_insert;
-- UPDATE TRIGGER 
DROP TRIGGER IF EXISTS aggregate_data_update ON usage_datausagerecord;
DROP TRIGGER IF EXISTS aggregate_voice_update ON usage_voiceusagerecord;
DROP FUNCTION IF EXISTS aggregate_object_update;
-- DELETE TRIGGER 
DROP TRIGGER IF EXISTS aggregate_data_delete ON usage_datausagerecord;
DROP TRIGGER IF EXISTS aggregate_voice_delete ON usage_voiceusagerecord;
DROP FUNCTION IF EXISTS aggregate_object_delete;
