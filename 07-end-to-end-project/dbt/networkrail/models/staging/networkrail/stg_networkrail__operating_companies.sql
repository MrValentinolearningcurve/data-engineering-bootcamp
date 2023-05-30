with

source as (

    select * from {{ ref('operating_companies') }}

)

, final as (

    select
        toc_id
        , company_name

    from source

)

select * from final