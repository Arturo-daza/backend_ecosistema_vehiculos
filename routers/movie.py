# from fastapi import APIRouter, Path, Query,HTTPException, status, Request, Depends
# from fastapi.responses import JSONResponse
# from middlewares.jwt_bearer import JWTBearer
# # from schemas.movie import Movie
# from typing import List
# from services.movie import MovieModel 

# movie_router = APIRouter()

# movies = [
#   {
#     "year": "1994",
#     "rating": "8.6",
#     "title": "The Shawshank Redemption",
#     "id": 1,
#     "category": "Drama",
#     "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
#   },
#   {
#     "year": "1994",
#     "rating": "9.2",
#     "title": "The Godfather",
#     "id": 2,
#     "category": "Crime",
#     "overview": "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son."
#   },
#   {
#     "year": "1994",
#     "rating": "8.5",
#     "title": "Pulp Fiction",
#     "id": 3,
#     "category": "Crime",
#     "overview": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
#   },
#   {
#     "year": "1994",
#     "rating": "8.7",
#     "title": "Forrest Gump",
#     "id": 4,
#     "category": "Drama",
#     "overview": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold through the perspective of an Alabama man with an IQ of 75."
#   },
#   {
#     "year": "1994",
#     "rating": "8.9",
#     "title": "Schindler's List",
#     "id": 5,
#     "category": "Biography",
#     "overview": "In German-occupied Poland during World War II, industrialist Oskar Schindler becomes concerned for his Jewish workforce after the start of the Holocaust."
#   },
#   {
#     "year": "1994",
#     "rating": "8.5",
#     "title": "The Lion King",
#     "id": 6,
#     "category": "Animation",
#     "overview": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."
#   },
#   {
#     "year": "1994",
#     "rating": "8.9",
#     "title": "The Usual Suspects",
#     "id": 7,
#     "category": "Crime",
#     "overview": "A sole survivor tells of the twisty events leading up to a horrific gun battle on a boat, which began when five criminals met at a police lineup."
#   },
#   {
#     "year": "1994",
#     "rating": "8.3",
#     "title": "Léon: The Professional",
#     "id": 8,
#     "category": "Crime",
#     "overview": "Mathilda, a twelve-year-old girl, is the only survivor of a family of drug dealers. She is rescued by Léon, a hitman."
#   },
#   {
#     "year": "1994",
#     "rating": "8.3",
#     "title": "The Terminator",
#     "id": 9,
#     "category": "Action",
#     "overview": "In the post-apocalyptic future, a cyborg is sent back in time to kill Sarah Connor, a young woman whose unborn son is the key to humanity's survival."
#   },
#   {
#     "year": "1994",
#     "rating": "8.4",
#     "title": "The Matrix",
#     "id": 10,
#     "category": "Action",
#     "overview": "When computer hacker Neo is contacted by mysterious rebels, he uncovers the shocking truth: that he is living in a simulated reality."
#   }
# ]

# @movie_router.get("/movies", tags=['movies'], response_model= List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
# def get_movies():
#     return JSONResponse(status_code=200, content=movies)

# @movie_router.get('/movies/{id}', tags=['movies'])
# def get_movie(id: int):
#     for item in movies:
#         if item["id"] == id:
#             return JSONResponse(content=item)
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró la película")    
    
# @movie_router.get("/movies/", tags = ['movies'], response_model= List[Movie])
# def get_movies_by_category(category:str = Query(min_length= 5, max_length=15)) -> List[Movie]:
#     data = [item for item in movies if item['category']== category]
#     return JSONResponse(content=data)


# @movie_router.post("/", tags=["movies"], response_model=dict, status_code=201)
# def create_movie(movie: Movie) -> dict:
#     # Verifica si ya existe una película con el mismo ID
#     if any(m['id'] == movie.id for m in movies):
#         raise HTTPException(status_code=400, detail="Movie with this ID already exists")
    
#     # Convierte el objeto Pydantic a un diccionario y lo añade a la lista
#     movie_dict = movie.model_dump()
#     movies.movie_routerend(movie_dict)
#     return JSONResponse(content={"message": "Movie created"}, status_code=201)

# @movie_router.put('/movies/{id}', tags = ['movies'], response_model=dict, status_code=200)
# def update_movie(id: int, movie: Movie):
#   for item in movies:
#       if item['id'] == id:
#         item['title'] = movie.title
#         item['overview'] = movie.overview
#         item['year'] = movie.year
#         item['rating'] = movie.rating
#         item['category'] = movie.category
#         return JSONResponse(status_code=200, content={"Message": "Se ha modificado la película"})

# @movie_router.delete('/movies/{id}', tags = ['movies'], response_model=dict,status_code=200)
# def delete_movie(id: int):
#   for item in movies:
#     if item["id"] == id:
#       movies.remove(item)
#       return JSONResponse(status_code=200,content={"Message": "Se ha Eliminado la película"})

