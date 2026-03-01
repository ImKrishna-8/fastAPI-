from fastapi import FastAPI,Depends,HTTPException
from database import engine
from sqlmodel import SQLModel,select,Session
import auth
from auth import get_current_user
from models import User
from models import RecipeCreate,Recipe
app = FastAPI()
app.include_router(auth.router)

@app.on_event('startup')
def startup():
    SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post('/recipes')
def add_recipe(recipe: RecipeCreate,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    if user:
        db_recipe = Recipe(title=recipe.title,description=recipe.description,owner_id=user["userid"]) # type: ignore
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return "added succesfully"

@app.get('/recipes')
def get_all_recipes(db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        db_recipes = db.exec(select(Recipe).where(Recipe.owner_id == user['userid'])).all()
        if not db_recipes:
            raise HTTPException(status_code=200,detail='no recipes found')
        return db_recipes



@app.get('/recipes/{id}')
def get_one_recipe(id:int,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        db_recipe = db.exec(select(Recipe).where(Recipe.id == id)).first()
        if db_recipe:
            if db_recipe.owner_id == user['userid']:
                return db_recipe
            raise HTTPException(status_code=401,detail='this recipe not belongs to you')
        raise HTTPException(status_code=404,detail='no recipe Found')


@app.put('/recipes/{id}')
def update_recipe(id:int,recipe:RecipeCreate,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        db_recipe = db.exec(select(Recipe).where(Recipe.id == id)).first()
        if db_recipe:
            if db_recipe.owner_id == user['userid']:
                db_recipe.title = recipe.title
                db_recipe.description = recipe.description
                db.commit()
                return "Updated Successfully"
            raise HTTPException(status_code=401,detail='this recipe is not belongs to you')
        raise HTTPException(status_code=404,detail='no recipe Found')
        
@app.delete('/recipes/{id}')
def delete_recipe(id:int,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        db_recipe = db.exec(select(Recipe).where(Recipe.id == id)).first()
        if db_recipe:
            if db_recipe.owner_id == user['userid']:
                db.delete(db_recipe)
                db.commit()
                return "Deleted Successfully"
            raise HTTPException(status_code=401,detail='this recipe is not belongs to you')
        raise HTTPException(status_code=200,detail='recipe not found with this id')