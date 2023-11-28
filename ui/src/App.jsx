import { useState, useEffect } from 'react'
import axios from 'axios'
import MovieList from './components/movie-list/movie-list.component'
import './App.css'


function App() {
  const [myMovies, setMyMovie] = useState([])
  const [page, setPage] = useState(1)
  const [numberOfPages, setNumberOfPages] = useState(1)
  const pageSize = 50;

  async function getMyMovies(){
    let config = {
      headers: {
        Authorization: "Token 14f3d5f19622f3719a6bf5da579a94fb61b9f5e4",
      },
    };
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/movie_short/?page=" + page,
        config
      );
      let movies = await response.data.results;
      setMyMovie(movies);
    } catch (error) {
      alert("ошибка в парсе кп");
    }
  }

  async function getMovies(){
    let config = {
      headers: {
        "X-API-KEY": "3W0ZPKY-H5XM7X8-KRB88NB-QSF7VJ5",
      },
    };
    try {
      for (var k = 50; k < 75; k++){
        console.log("Начинаю получать фильмы с " + k + " страницы");
        const response = await axios.get(
          "https://api.kinopoisk.dev/v1.4/movie?page=" + k + "&limit=50&selectFields=id&selectFields=name&selectFields=names&selectFields=description&selectFields=slogan&selectFields=type&selectFields=year&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=premiere&notNullFields=id&notNullFields=name&notNullFields=description&notNullFields=slogan&notNullFields=type&notNullFields=year&notNullFields=movieLength&notNullFields=genres.name&notNullFields=countries.name&notNullFields=poster.url&notNullFields=persons.id&notNullFields=persons.name&notNullFields=persons.enName&notNullFields=persons.photo&notNullFields=persons.profession&notNullFields=persons.enProfession&notNullFields=premiere.world&type=movie",
          config
        );
        console.log(response.data.docs);
        for (var i = 0; i < 50; i++){
          console.log("Отправляю " + i + "фильм")
          await postMovie(response.data.docs[i])
          console.log("Загрузил " + i + "фильм")
      }
      }
      
    } catch (error) {
      alert(error.message);
    }
  }

  async function postMovie(movie) {
    let data = {
      movies: movie,
    };
    let config = {
      headers: {
        Authorization: "Token 14f3d5f19622f3719a6bf5da579a94fb61b9f5e4",
      },
    };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/movie/addMovies/",
        data,
        config
      );
      console.log(response.status);
    } catch (error) {
      alert(error.message);
    }
  }
  
  function show() {
    console.log(myMovies);
  }

  function next() {
    setPage(page + 1);
  }

  function previos() {
    if(page - 1 != 0){
      setPage(page - 1);
    } 
  }
  
  useEffect(()=>{
    getMyMovies();
    console.log("вызвал юз эффект");
  }, [page]);
  

  return (
    <div>
      <button onClick={getMovies}>Получить фильм</button>
      <button onClick={next}>Следующая страница</button>
      <button onClick={previos}>Предыдущая страница</button>
      <h1>My Appp ahah</h1>
      <MovieList movies={myMovies} page={page} pageSize={pageSize}/>
      
      <button onClick={show}>Показать фильм</button>
    </div>
  )
}

export default App
