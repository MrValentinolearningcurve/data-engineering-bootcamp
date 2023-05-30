with

fct_movements as (

    select * from {{ ref('fct_movements') }}

)

, variation_status_agg_for_each_train as (

    select
        train_id
        , company_name
        , array_agg(variation_status) as variation_statuses

    from fct_movements
    group by 1, 2

)

select
    train_id
    , company_name

from variation_status_agg_for_each_train as v
where
    'LATE' not in unnest(v.variation_statuses)
    and 'OFF ROUTE' not in unnest(v.variation_statuses)
