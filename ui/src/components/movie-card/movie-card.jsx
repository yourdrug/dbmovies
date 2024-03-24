import { Link } from 'react-router-dom';
import { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import './movie-card.css'
import Modal from '../modal/modal';
import LoginForm from '../login-form/login-form';

import { UserContext } from '../../context/user.context';

const MovieCard = ({ movie, index }) => {
    const [selectedRating, setSelectedRating] = useState(movie.user_rating);
    const [like, setLike] = useState(movie.user_like);
    const [isWatched, setIsWatched] = useState(movie.user_is_watched);
    const [isInBookmarks, setIsInBookmarks] = useState(movie.user_is_in_bookmark);
    const [showRatingOptions, setShowRatingOptions] = useState(false);
    const { token } = useContext(UserContext)
    const [active, setActive] = useState(false);
    const [showSelectForAlbums, setShowSelectForAlbums] = useState(false);

    async function updateRate (id, rating) {
        let config = {
            headers: {
                Authorization: "Token " + token,
            },
        };
        let data = {
            'rate': rating,
        };
        try {
            await axios.patch(`http://127.0.0.1:8000/movie_relation/${id}/`, data, config);
        } catch (error) {
            alert(error.message);
        }
    }

    async function updateLike (id, current_like) {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'like': !current_like,
        };
        try {
            const response = await axios.patch(
              `http://127.0.0.1:8000/movie_relation/${id}/`, data, config
            );
            console.log(response);
        } catch (error) {
            alert(error.message);
        }
    }

    async function updateIsWatched (id, current_state) {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'is_watched': !current_state,
        };
        try {
            const response = await axios.patch(
              `http://127.0.0.1:8000/movie_relation/${id}/`, data, config
            );
            console.log(response);
        } catch (error) {
            alert(error.message);
        }
    }

    async function updateBookmarks (id, current_state) {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'in_bookmarks': !current_state,
        };
        try {
            const response = await axios.patch(
              `http://127.0.0.1:8000/movie_relation/${id}/`, data, config
            );
            console.log(response);
        } catch (error) {
            alert(error.message);
        }
    }

    useEffect(()=>{
        setSelectedRating(movie.user_rating);
    }, [movie]);

    const handleRatingClick = (id, rating) => {
        setSelectedRating(rating);
        setShowRatingOptions(false); // Закрываем варианты оценок после выбора
        updateRate(id, rating);
    };

    const handleLikeClick = (id, current_like) => {
        if(token){
            setLike(!like);
            updateLike(id, current_like);
        }
        else{
            setActive(true);
        }
        
    };
    
    const handleButtonClick = () => {
        if(token !== null){
            setShowRatingOptions(!showRatingOptions); // Инвертируем видимость вариантов оценок
        }
        else{
            setActive(true);
        }
        
    };

    const markAsWatchedButtonClick = (id, currentState) => {
        if(token){
            setIsWatched(!isWatched);
            updateIsWatched(id, currentState);
        }
        else{
            setActive(true);
        }
    };

    const markInBookmarksButtonClick = (id, currentState) => {
        if(token){
            setIsInBookmarks(!isInBookmarks);
            updateBookmarks(id, currentState);
        }
        else{
            setActive(true);
        }
    };

    const getRatingColor = (rating) => {
        if (rating >= 1 && rating <= 5) {
          return 'red-set-rate';
        } else if (rating >= 6 && rating <= 7) {
          return 'gray-set-rate';
        } else {
          return 'green-set-rate';
        }
    };

    let className="movie-rate"
    if (movie.rating >= 7.5){
        className += '-good';
    }

    else if (movie.rating >= 5.5 && movie.rating <= 7.5){
        className += '-average';
    }

    else{
        className += '-bad'
    }

    return (
        <div className={isWatched ? 'movie-card watched' : 'movie-card'}>
            <div className="number"> {index} </div>
                <Link className="poster" to={`/movies/${movie.id}`}>
                    <img src={movie.poster} />
                </Link>
                <Link className="movie-info" to={`/movies/${movie.id}`}>
                    <div className="movie-name">{ movie.name }</div>
                    <div className="movie-desc"> { movie.year }, { movie.watch_time } мин.</div>
                    <div className="movie-more-desc"> { movie.country.split(",")[0] } | { movie.genres[0].name }
                        &nbsp;Режиссёр: { movie.crew.filter((profession) => profession.slug == 'director')[0].person.name } <br />
                        <br /> В ролях: { movie.crew.filter((profession) => profession.slug == 'actor')[0].person.name },&nbsp;
                                        { movie.crew.filter((profession) => profession.slug == 'actor')[1].person.name }</div>
                </Link>
            <div className="additional-info">
                <div className={className}> {movie.rating} </div> 
                <div className="count-rates">{ movie.annotated_count_rate }</div>
                <div className='my-own-rating'>
                    {selectedRating ? (
                        <div className={`selected-rating ${getRatingColor(selectedRating)}`}
                        onClick={() => handleRatingClick(movie.id, null)}> {selectedRating} </div>
                    ) : (
                        <button className="movie-card-set-rate" onClick={handleButtonClick}/>
                    )}
                    {showRatingOptions && !selectedRating &&(
                    <div className='choices-for-marks'>
                        {[...Array(10).keys()].map((index) => {
                        const rating = index + 1;
                        let colorClass;

                        if (rating >= 1 && rating <= 5) {
                            colorClass = 'red';
                        } else if (rating >= 6 && rating <= 7) {
                            colorClass = 'grey';
                        } else {
                            colorClass = 'green';
                        }

                        return (
                            <span
                                key={rating}
                                className={`rating-digit ${colorClass} ${selectedRating === rating ? 'selected' : ''}`}
                                onClick={() => handleRatingClick(movie.id ,rating)}> {rating} </span>
                        );
                        })}
                    </div>
                )}
                </div>
                <div className='like-option-at-movie'>
                    {like ? (
                        <div className='like-pressed-at-movie' onClick={() => handleLikeClick(movie.id, like)}/>
                    ) : (
                        <div className="like-not-pressed-at-movie" onClick={() => handleLikeClick(movie.id, like)}/>
                    )}
                </div>
                <button className="movie-card-additional-options" onClick={()=> setShowSelectForAlbums(!showSelectForAlbums)}/>
                {showSelectForAlbums && 
                    <div className='select-options-for-movies'>
                        <button className='choose-for-album-btn' onClick={()=> markAsWatchedButtonClick(movie.id, isWatched)}> 
                            Просмотрен 
                            {isWatched ? <img className='is-movie-watched' src='https://cdn-icons-png.flaticon.com/512/5191/5191458.png'/> 
                                        : <img className='is-movie-watched' src='https://cdn-icons-png.flaticon.com/256/876/876769.png'/>}
                        </button>
                        <button className='choose-for-album-btn' onClick={()=> markInBookmarksButtonClick(movie.id, isInBookmarks)}> 
                        Избранное 
                            {isInBookmarks && <img className='is-in-bookmarks' src='https://cdn-icons-png.flaticon.com/512/1828/1828710.png'/>}
                        </button>
                    </div>      
                }
            </div>
            <Modal active={active} setActive={setActive}>
                <LoginForm />
            </Modal>
        </div>
        
    );
  };
  
  export default MovieCard;