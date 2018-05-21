# brokerify
Un pequeño script que utilizo para tomar decisiones de inversión a largo plazo en la bolsa.

# migrations
## create auto
ex: http://alembic.zzzcomputing.com/en/latest/autogenerate.html
`alembic revision --autogenerate -m "Init tables"`

## new
ex: http://alembic.zzzcomputing.com/en/latest/tutorial.html
`alembic revision -m "Add a column"`

## Run migration
`alembic upgrade head`

## Downgrade
`alembic downgrade base`
