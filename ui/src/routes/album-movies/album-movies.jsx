import { Link, useParams } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import MovieList from '../../components/movie-list/movie-list';
import axios from 'axios';
import { UserContext } from '../../context/user.context';

const AlbumMovies = () => {
  const { currentUser, token } = useContext(UserContext)
  const [likedMovies, setLikedMovies] = useState([])
  const [bookmarkedMovies, setBookmarkedMovies] = useState([])
  const [watchedMovies, setWatchedMovies] = useState([])
  const [willWatchMovies, setWillWatchedMovies] = useState([])

  const params = useParams();
  let albumName = params.albumName;

async function getLikedMoives(){
  if (token != null){
    var config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
  }
  
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/movie_short/liked_movies", config
    );
    let info = await response.data;
    setLikedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getWatchedMoives(){
  if (token != null){
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
    let info = await response.data;
    setWatchedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getBookmarksMoives(){
  if (token != null){
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
    let info = await response.data;
    setBookmarkedMovies(info);
  } catch (error) {
    alert("ошибка в получении данных с сервера");
  }
}

async function getWillWatchMoives(){
  if (token != null){
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
    let info = await response.data;
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
}, []);

  return (
    <div className="main-wrapper">
      {albumName == 'liked' && <MovieList className='movies-list' movies={likedMovies} page={1} pageSize={50}/>}
      {albumName == 'watched' && <MovieList className='movies-list' movies={watchedMovies} page={1} pageSize={50}/>}
      {albumName == 'bookmarks' && <MovieList className='movies-list' movies={bookmarkedMovies} page={1} pageSize={50}/>}
      {albumName == 'will-watch' && <MovieList className='movies-list' movies={willWatchMovies} page={1} pageSize={50}/>}
    </div>
  );
};

export default AlbumMovies;