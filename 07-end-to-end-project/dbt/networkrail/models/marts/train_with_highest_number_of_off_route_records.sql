with

fct_movements as (

    select * from {{ ref('fct_movements') }}

)

select
    train_id
    , count(1) as record_count

from fct_movements
where variation_status = 'OFF ROUTE'
group by 1
order by 2 desc
limit 1
