import { Link } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../../context/user.context';
import LittleMovieCard from '../../components/movie-little-card/movie-little-card.component';

import axios from 'axios';
import './profile.styles.css'

const Profile = () => {
    const { currentUser, token } = useContext(UserContext)
    const [userInfo, setUserInfo] = useState([])
    const [movie, setMovie] = useState([])
    const [likedMovies, setLikedMovies] = useState([])
    const [bookmarkedMovies, setBookmarkedMovies] = useState([])
    const [watchedMovies, setWatchedMovies] = useState([])

    async function getMovie(){
      if (token != null){
        var config = {
          headers: {
            Authorization: "Token " + token,
          },
        };
      }
      
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/movie/randomMovie/", config
        );
        let info = await response.data;
        console.log("полученная информация " + JSON.stringify(info))
        setMovie(info);
      } catch (error) {
        alert("ошибка в получении данных с сервера");
      }
  }

    async function getUserInfo(){
        if (token != null){
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
          console.log("полученная информация " + JSON.stringify(info))
          setUserInfo(info);
          await getMovie();
          const { likedMovies, bookmarkedMovies, watchedMovies } = processMovies(info);
          setLikedMovies(likedMovies);
          setBookmarkedMovies(bookmarkedMovies);
          setWatchedMovies(watchedMovies);
          console.log(likedMovies);
        } catch (error) {
          alert("ошибка в получении данных с сервера");
        }
    }

    function processMovies(jsonData) {
      const likedMovies = [];
      const bookmarkedMovies = [];
      const watchedMovies = [];
    
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
      });
    
      return { likedMovies, bookmarkedMovies, watchedMovies };
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
                <div>{userInfo.total_likes}</div>
                <div>{userInfo.total_reviews}</div>
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
                    {likedMovies.length > 3 && (<button className='control-buttons'>Смотреть еще</button>)}
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
                    {bookmarkedMovies.length > 3 && (<button className='control-buttons'>Смотреть еще</button>)}
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
                    {watchedMovies.length > 3 && (<button className='control-buttons'>Смотреть еще</button>)}
              </div>
            </div>
          </div>
          <div className='buttons-for-control-page'>
            <button className='control-buttons'> Редактировать </button>
            <Link to='/chatting'><button className='control-buttons' >Cообщения </button></Link>
            <button className='control-buttons' onClick={()=> getMovie()}> Фильм на вечер </button>
            

          </div>
        </div>
         
          
      </div>
    )
}

export default Profile;