import { Link } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../../context/user.context';
import LittleMovieCard from '../../components/movie-little-card/movie-little-card';

import axios from 'axios';
import './profile.css'

const Profile = () => {
  const { currentUser, token, setCurrentUser, setToken, socket, setSocket } = useContext(UserContext)
  const [userInfo, setUserInfo] = useState([])
  const [likedMovies, setLikedMovies] = useState([])
  const [bookmarkedMovies, setBookmarkedMovies] = useState([])
  const [watchedMovies, setWatchedMovies] = useState([])
  const [willWatchMovies, setWillWatchMovies] = useState([])

  async function getUserInfo(){
    if (token){
      var config = {
        headers: {
          Authorization: "Token " + token,
        },
      };
    }
    
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/user_movie_relation", config
      );
      let info = await response.data;
      setUserInfo(info);
      const { likedMovies, bookmarkedMovies, watchedMovies, willWatchMovies } = processMovies(info);
      setLikedMovies(likedMovies);
      setBookmarkedMovies(bookmarkedMovies);
      setWatchedMovies(watchedMovies);
      setWillWatchMovies(willWatchMovies);
    } catch (error) {
      alert("ошибка в получении данных с сервера");
    }
  }

  function processMovies(jsonData) {
    const likedMovies = [];
    const bookmarkedMovies = [];
    const watchedMovies = [];
    const willWatchMovies = [];
  
    jsonData.main.forEach(item => {
      const movieData = item.movie;
  
      if (item.like) {
        likedMovies.push(movieData);
      }
  
      if (item.in_bookmarks) {
        bookmarkedMovies.push(movieData);
      }
  
      if (item.is_watched) {
        watchedMovies.push(movieData);
      }

      if (item.will_watch) {
        willWatchMovies.push(movieData);
      }
    });
  
    return { likedMovies, bookmarkedMovies, watchedMovies, willWatchMovies };
  }

  async function logout() {
    let data = { username: currentUser.username, password: localStorage.getItem("password")};
    let config = {
        headers: {
          Authorization: "Token " + token,
        },
      };
    axios.post("http://127.0.0.1:8000/auth/token/logout/", data, config)
        .then(() => {
            setCurrentUser(null);
            setToken(null);
        })
        .catch(error => {
            alert(error.message);
        });
}

  function handleLogoutClick(){
    logout();
    setCurrentUser(null);
    setToken(null);
    socket.close();
    setSocket(null);
    localStorage.setItem("token", null);
    localStorage.setItem("currentUser", null);
    localStorage.setItem("password", null);     
  }
  
  useEffect(()=>{
    getUserInfo();
  }, []);

  return(
    <div className='main-wrapper'>
      <div className='wrapper-for-profile'>
        <div className='profile-info-at-page'>
          <div className='avatar-and-labels-near'>
            <div>
              <img src={currentUser.image} width="200" height="200"/>
            </div>
            <div className='username-and-total-info-for-user'>
              <div>{currentUser.username}</div>
              <div className='user-info-total-parametrs'>
                <div>{userInfo.total_likes}</div>
                <img 
                  src='https://cdn-icons-png.flaticon.com/256/158/158722.png'
                  height={"30px"}
                  width={"30px"}/>
              </div>
              <div className='user-info-total-parametrs'>
                <div>{userInfo.total_reviews}</div>
                <img 
                  src='https://cdn-icons-png.flaticon.com/512/2182/2182946.png'
                  height={"40px"}
                  width={"40px"}/>
              </div>
            </div>
          </div>
          <div className='navigation-profile-btns'>
            <h2>Любимые фильмы</h2>
            <div className='users-liked-movies'>
              {likedMovies.length > 3
                ? likedMovies.slice(0, 3).map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))
                : likedMovies.map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))}
                  {likedMovies.length > 3 && 
                  (<Link to={`/profile/${currentUser.id}/liked`} style={{textDecoration: "none"}} className='control-buttons'>Смотреть еще</Link>)}
            </div>
            <h2> Избранное </h2>
            <div className='users-liked-movies'>
              {bookmarkedMovies.length > 3
                ? bookmarkedMovies.slice(0, 3).map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))
                : bookmarkedMovies.map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))}
                  {bookmarkedMovies.length > 3 && 
                  (<Link to={`/profile/${currentUser.id}/bookmarks`} style={{textDecoration: "none"}} className='control-buttons'>Смотреть еще</Link>)}
            </div>
            <h2>Просмотренные фильмы</h2>
            <div className='users-liked-movies'>
              {watchedMovies.length > 3
                ? watchedMovies.slice(0, 3).map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))
                : watchedMovies.map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))}
                  {watchedMovies.length > 3 && 
                  (<Link to={`/profile/${currentUser.id}/watched`} style={{textDecoration: "none"}} className='control-buttons'>Смотреть еще</Link>)}
            </div>
            <h2>Буду смотреть</h2>
            <div className='users-liked-movies'>
              {willWatchMovies.length > 3
                ? willWatchMovies.slice(0, 3).map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))
                : willWatchMovies.map((movie) => (
                  <LittleMovieCard key={movie.id} movie={movie} />
                ))}
                  {willWatchMovies.length > 3 && 
                  (<Link to={`/profile/${currentUser.id}/will-watch`} style={{textDecoration: "none"}} className='control-buttons'>Смотреть еще</Link>)}
            </div>
          </div>
        </div>
        <div className='buttons-for-control-page'>
          <Link style={{textDecoration: "none"}} to='/'><button className='control-buttons' onClick={()=>handleLogoutClick()}> Выйти </button></Link>
          <Link style={{textDecoration: "none"}} to='/profile/edit'><button className='control-buttons'> Редактировать </button></Link>
          <Link style={{textDecoration: "none"}} to='/chatting'><button className='control-buttons' >Cообщения </button></Link>
          <Link style={{textDecoration: "none"}} to='/random-movie'><button className='control-buttons'> Фильм на вечер </button></Link>
        </div>
      </div>       
    </div>
  )
}

export default Profile;