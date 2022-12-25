-- Create or replace will not work if parameters will change.
DROP PROCEDURE IF EXISTS create_aggregated_object;
CREATE PROCEDURE create_aggregated_object(
    type_of_usage VARCHAR,
    subscription_id INT,
    price DECIMAL, 
    usage_date DATE,
    used INT 
)
LANGUAGE plpgsql
AS $$
BEGIN
-- Create new usage_record
    INSERT INTO usage_usagerecord(type_of_usage, subscription_id, price, usage_date, used)
    VALUES (type_of_usage, subscription_id, price, usage_date::DATE, used);
END;
$$;


DROP PROCEDURE IF EXISTS update_aggregated_object;
CREATE PROCEDURE update_aggregated_object(
    instance_id INT,
    new_price DECIMAL, 
    new_used INT    
)
LANGUAGE plpgsql
AS $$
BEGIN
-- Update old usage usage_record price and used fields
    UPDATE usage_usagerecord SET
        price = price + new_price,
        used = used + new_used
    WHERE id = instance_id;
END;
$$;




-- INSERT TRIGGER
DROP TRIGGER IF EXISTS aggregate_data_insert ON usage_datausagerecord;
DROP TRIGGER IF EXISTS aggregate_voice_insert ON usage_voiceusagerecord;
DROP FUNCTION IF EXISTS aggregate_object_insert;
CREATE FUNCTION aggregate_object_insert()
    RETURNS TRIGGER AS $$
DECLARE
    usage_type VARCHAR;
    used INT;
    aggregated_instance usage_usagerecord%ROWTYPE;
BEGIN
    -- On INSERT create/update aggregated instance for data and voice usage_types
    -- Based on usage_type get used fields
    usage_type := TG_ARGV[0];
    IF usage_type = 'data' THEN
        used := NEW.kilobytes_used;
    ELSE
        used := NEW.seconds_used;
    END IF;
    
    -- Get usage_record by type_of_usage subscription_id and usage_data. 
    SELECT * INTO aggregated_instance FROM usage_usagerecord WHERE 
        type_of_usage = usage_type
        and subscription_id = NEW.subscription_id_id
        and usage_date = NEW.usage_date::date;

    IF aggregated_instance.id IS NULL THEN
        CALL create_aggregated_object(
            usage_type, 
            NEW.subscription_id_id, 
            NEW.price, 
            NEW.usage_date::date, 
            used
        );
    ELSE
        CALL update_aggregated_object(
            aggregated_instance.id,
            NEW.price, 
            used
        );  
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';
CREATE TRIGGER aggregate_data_insert BEFORE INSERT on usage_datausagerecord FOR EACH ROW EXECUTE FUNCTION aggregate_object_insert('data');
CREATE TRIGGER aggregate_voice_insert BEFORE INSERT on usage_voiceusagerecord FOR EACH ROW EXECUTE FUNCTION aggregate_object_insert('voice');




-- UPDATE TRIGGER
DROP TRIGGER IF EXISTS aggregate_data_update ON usage_datausagerecord;
DROP TRIGGER IF EXISTS aggregate_voice_update ON usage_voiceusagerecord;
DROP FUNCTION IF EXISTS aggregate_object_update;
CREATE FUNCTION aggregate_object_update()
    RETURNS TRIGGER AS $$
DECLARE
    usage_type VARCHAR;
    aggregated_used INT;
    aggregated_price INT;
    aggregated_instance usage_usagerecord%ROWTYPE;
BEGIN
    -- On UPDATE create/update aggregated instance for data and voice usage_types
    -- Based on usage_type get used fields
    usage_type := TG_ARGV[0];
    IF usage_type = 'data' THEN
        aggregated_used := NEW.kilobytes_used;
    ELSE
        aggregated_used := NEW.seconds_used;
    END IF;
    
    -- Get usage_record by type_of_usage subscription_id and usage_data. 
    SELECT * INTO aggregated_instance FROM usage_usagerecord WHERE 
        type_of_usage = usage_type
        and subscription_id = NEW.subscription_id_id
        and usage_date = NEW.usage_date::date;

    IF aggregated_instance.id IS NULL THEN
        CALL create_aggregated_object(
            usage_type, 
            NEW.subscription_id_id, 
            NEW.price, 
            NEW.usage_date::date, 
            aggregated_used
        );
    ELSE
        -- ON UPDATE delete previous instance price and aggregated_used fields 
        IF usage_type = 'data' THEN
            aggregated_price = NEW.price - OLD.price;
            aggregated_used = aggregated_used - OLD.kilobytes_used;
        ELSE
            aggregated_price = NEW.price - OLD.price;
            aggregated_used = aggregated_used - OLD.seconds_used;
        END IF;
        CALL update_aggregated_object(
            aggregated_instance.id,
            aggregated_price, 
            aggregated_used
        );  
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';
CREATE TRIGGER aggregate_data_update BEFORE UPDATE on usage_datausagerecord FOR EACH ROW EXECUTE FUNCTION aggregate_object_update('data');
CREATE TRIGGER aggregate_voice_update BEFORE UPDATE on usage_voiceusagerecord FOR EACH ROW EXECUTE FUNCTION aggregate_object_update('voice');



-- DELETE TRIGGER
DROP TRIGGER IF EXISTS aggregate_data_delete ON usage_datausagerecord;
DROP TRIGGER IF EXISTS aggregate_voice_delete ON usage_voiceusagerecord;
DROP FUNCTION IF EXISTS aggregate_object_delete;
CREATE FUNCTION aggregate_object_delete()
    RETURNS TRIGGER AS $$
DECLARE
    aggregated_used INT;
    usage_type VARCHAR;
    aggregated_instance usage_usagerecord%ROWTYPE;
BEGIN
    -- On DELETE delete from aggregated instance for data and voice usage_types
    -- Based on usage_type get used fields
    usage_type := TG_ARGV[0];
    IF usage_type = 'data' THEN
        aggregated_used := OLD.kilobytes_used;
    ELSE
        aggregated_used := OLD.seconds_used;
    END IF;
    
    -- Get usage_record by type_of_usage, subscription_id and usage_data. 
    SELECT * INTO aggregated_instance FROM usage_usagerecord WHERE 
        type_of_usage = usage_type
        and subscription_id = OLD.subscription_id_id
        and usage_date = OLD.usage_date::date;

    IF aggregated_instance.id IS NOT NULL THEN
        CALL update_aggregated_object(
            aggregated_instance.id,
            -OLD.price, 
            -aggregated_used
        ); 
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE 'plpgsql';
CREATE TRIGGER aggregate_data_delete BEFORE DELETE on usage_datausagerecord FOR EACH ROW EXECUTE FUNCTION aggregate_object_delete('data');
CREATE TRIGGER aggregate_voice_delete BEFORE DELETE on usage_voiceusagerecord FOR EACH ROW EXECUTE FUNCTION aggregate_object_delete('voice');
