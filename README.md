Celery გასაშვებად საჭიროა:

დააყენე პაკეტები
```
pip install -r requirements_new
```
გააკეთე მიგრაციები

ცალკე სცრინის ტერმინალში გაუშვი
```
celery -A world_map worker --loglevel=info
```

კიდე ცალკე ტერმინალში
```
celery -A world_map beat --loglevel=info
```
