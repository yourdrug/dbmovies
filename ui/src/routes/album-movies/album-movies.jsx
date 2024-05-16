import { Link, useParams } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import MovieList from '../../components/movie-list/movie-list';
import Pagination from '../../components/pagination-page/pagination-page';
import { toast } from 'react-toastify';
import axios from 'axios';
import { UserContext } from '../../context/user.context';

const pageSize = 50;

const AlbumMovies = () => {
  const { currentUser, token } = useContext(UserContext)
  const [likedMovies, setLikedMovies] = useState([])
  const [bookmarkedMovies, setBookmarkedMovies] = useState([])
  const [watchedMovies, setWatchedMovies] = useState([])
  const [willWatchMovies, setWillWatchedMovies] = useState([])
  const [top_250, setTop250] = useState([])
  const [top_500, setTop500] = useState([])
  const [admins_top, setAdminsTop] = useState([])

  const [page, setPage] = useState(1)
  const [numberOfPages, setNumberOfPages] = useState(1)

  const params = useParams();
  let albumName = params.albumName;

async function getLikedMoives(){
  if (token){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/movie_short/liked_movies/?page=${page}`, config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setLikedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getWatchedMoives(){
  if (token){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/watched_movies", config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setWatchedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getBookmarksMoives(){
  if (token){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/bookmarked_movies", config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setBookmarkedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getWillWatchMoives(){
  if (token){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/will_watch_movies", config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setWillWatchedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getTop250(){
  if (currentUser){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/get_top_250", config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setTop250(info);
  } catch (error) {
    toast.warn('Технические неполадки. Попробуйте позже.');
  }
}

async function getTop500(){
  if (currentUser){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/get_top_500", config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setTop500(info);
  } catch (error) {
    toast.warn('Технические неполадки. Попробуйте позже.');
  }
}

async function getAdminsTop(){
  if (currentUser){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/get_random_20", config
    );
    let info = await response.data.results;
    let count =  await response.data.count;
    let res = Math.ceil(count / pageSize)
    setNumberOfPages(res);
    setAdminsTop(info);
  } catch (error) {
    toast.warn('Технические неполадки. Попробуйте позже.');
  }
}

useEffect(()=>{
  switch(albumName){
    case 'liked':
      getLikedMoives();
      break;
    case 'watched':
      getWatchedMoives();
      break;
    case 'bookmarks':
      getBookmarksMoives();
      break;
    case 'will-watch':
      getWillWatchMoives();
      break;
    case 'top-250':
      getTop250();
      break;
    case 'top-500':
      getTop500();
      break;
    case 'admins-top':
      getAdminsTop();
      break;
  }
}, [page]);

  return (
    <div className="main-wrapper">
      <Pagination setPage={setPage} page={page} numberOfPages={numberOfPages}/>
      {albumName == 'liked' && <MovieList className='movies-list' movies={likedMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'watched' && <MovieList className='movies-list' movies={watchedMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'bookmarks' && <MovieList className='movies-list' movies={bookmarkedMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'will-watch' && <MovieList className='movies-list' movies={willWatchMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'top-250' && <MovieList className='movies-list' movies={top_250} page={page} pageSize={pageSize}/>}
      {albumName == 'top-500' && <MovieList className='movies-list' movies={top_500} page={page} pageSize={pageSize}/>}
      {albumName == 'admins-top' && <MovieList className='movies-list' movies={admins_top} page={page} pageSize={pageSize}/>}
    </div>
  );
};

export default AlbumMovies;