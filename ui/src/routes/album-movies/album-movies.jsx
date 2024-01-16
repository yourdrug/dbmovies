import { Link, useParams } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import MovieList from '../../components/movie-list/movie-list';
import Pagination from '../../components/pagination-page/pagination-page';
import axios from 'axios';
import { UserContext } from '../../context/user.context';

const pageSize = 50;

const AlbumMovies = () => {
  const { currentUser, token } = useContext(UserContext)
  const [likedMovies, setLikedMovies] = useState([])
  const [bookmarkedMovies, setBookmarkedMovies] = useState([])
  const [watchedMovies, setWatchedMovies] = useState([])
  const [willWatchMovies, setWillWatchedMovies] = useState([])

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
  }
}, [page]);

  return (
    <div className="main-wrapper">
      <Pagination setPage={setPage} page={page} numberOfPages={numberOfPages}/>
      {albumName == 'liked' && <MovieList className='movies-list' movies={likedMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'watched' && <MovieList className='movies-list' movies={watchedMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'bookmarks' && <MovieList className='movies-list' movies={bookmarkedMovies} page={page} pageSize={pageSize}/>}
      {albumName == 'will-watch' && <MovieList className='movies-list' movies={willWatchMovies} page={page} pageSize={pageSize}/>}
    </div>
  );
};

export default AlbumMovies;