import { useState, useEffect, useContext } from 'react'
import axios from 'axios'
import MovieList from '../../components/movie-list/movie-list.component';
import Pagination from '../../components/pagination-page/pagination-page.component';
import { UserContext } from '../../context/user.context';
import './movies.styles.css'

const pageSize = 50;

function Movies() {
  const [myMovies, setMyMovie] = useState([])
  const [page, setPage] = useState(1)
  const [numberOfPages, setNumberOfPages] = useState(1)
  
  const { token } = useContext(UserContext) 
  
  async function getMyMovies(){
    if (token != null){
      var config = {
        headers: {
          Authorization: "Token " + token,
        },
      };
    }
    
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/movie_short/?page=" + page, config
      );
      let movies = await response.data.results;
      let count =  await response.data.count;
      let res = Math.ceil(count / pageSize)
      setNumberOfPages(res);
      setMyMovie(movies);
      console.log(token);
      console.log(myMovies);
    } catch (error) {
      alert("ошибка в получении данных с сервера");
    }
  }

  async function getMovies(){
    let config = {
      headers: {
        "X-API-KEY": "3W0ZPKY-H5XM7X8-KRB88NB-QSF7VJ5",
      },
    };
    try {
      for (var k = 1; k < 6; k++){
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
        Authorization: "Token 9adeceea3d89a408b5c8f3157076e756ef9b98ca",
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
  
  function next(){
    setPage(page + 1);
  }

  useEffect(()=>{
    console.log(myMovies);
    getMyMovies();
    console.log(myMovies);
  }, [page, token]);

  return (
    <div className='main-wrapper'>
      <button onClick={getMovies}>Получить фильм</button>
      <button onClick={next}>Следующая страница</button>
      <Pagination setPage={setPage} page={page} numberOfPages={numberOfPages}/>
      <MovieList className='movies-list' movies={myMovies} page={page} pageSize={pageSize}/>    
    </div>
  )
}

export default Movies;