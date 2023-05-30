with

movements as (

    select * from {{ ref('stg_networkrail__movements') }}

)

, operating_companies as (

    select * from {{ ref('stg_networkrail__operating_companies') }}

)

, joined as (

    select
        event_type
        , gbtt_timestamp_utc
        , original_loc_stanox
        , planned_timestamp_utc
        , timetable_variation
        , original_loc_timestamp_utc
        , current_train_id
        , delay_monitoring_point
        , next_report_run_time
        , reporting_stanox
        , actual_timestamp_utc
        , correction_ind
        , event_source
        , train_file_address
        , platform
        , division_code
        , train_terminated
        , train_id
        , offroute_ind
        , variation_status
        , train_service_code
        , m.toc_id as toc_id
        , oc.company_name as company_name
        , loc_stanox
        , auto_expected
        , direction_ind
        , route
        , planned_event_type
        , next_report_stanox
        , line_ind

    from movements as m
    left join operating_companies as oc
        on m.toc_id = oc.toc_id

)

, final as (

    select
        event_type
        , gbtt_timestamp_utc
        , original_loc_stanox
        , planned_timestamp_utc
        , timetable_variation
        , original_loc_timestamp_utc
        , current_train_id
        , delay_monitoring_point
        , next_report_run_time
        , reporting_stanox
        , actual_timestamp_utc
        , correction_ind
        , event_source
        , train_file_address
        , platform
        , division_code
        , train_terminated
        , train_id
        , offroute_ind
        , variation_status
        , train_service_code
        , toc_id
        , company_name
        , loc_stanox
        , auto_expected
        , direction_ind
        , route
        , planned_event_type
        , next_report_stanox
        , line_ind

    from joined

)

select * from final