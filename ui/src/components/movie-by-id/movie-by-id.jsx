import { useEffect, useState, useContext, useRef } from "react";
import { useParams, Link } from "react-router-dom";

import CriticImage from '../../assets/critic.jpg'

import axios from "axios";
import { format, parseISO } from 'date-fns';
import { ru } from 'date-fns/locale';

import { UserContext } from "../../context/user.context";

import './movie-by-id.css'

const MovieById = () => {
    const [movie, setMovie] = useState(null)
    const [inputMessage, setInputMessage] = useState("");
    const { currentUser, token } = useContext(UserContext) 
    const [selectedRating, setSelectedRating] = useState(null);
    const [showRatingOptions, setShowRatingOptions] = useState(false);

    const params = useParams();
    let movieId = params.id;

    async function sendReview () {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'review': inputMessage,
        };
        try {
            const response = await axios.patch(
              `http://127.0.0.1:8000/movie_relation/${movieId}/`, data, config
            );
            setInputMessage("");
        } catch (error) {
            alert(error.message);
        }
    }

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

    const choicesRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
        if (choicesRef.current && !choicesRef.current.contains(event.target)) {
            setShowRatingOptions(false);
        }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleRatingClick = (id, rating) => {
        setSelectedRating(rating);
        setShowRatingOptions(false); // Закрываем варианты оценок после выбора
        updateRate(id, rating);
    };

    const handleButtonClick = () => {
        if(token !== null){
            setShowRatingOptions(!showRatingOptions); // Инвертируем видимость вариантов оценок
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
    
    async function getMovieById(){
        let config = {
            headers: {
                Authorization: "Token " + token,
            },
        };
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/movie/${movieId}`, config
          );
          let movie = await response.data;
          console.log(response.data)
          setMovie(movie);
          setSelectedRating(movie.user_rating);
        } catch (error) {
          alert("ошибка в получении данных с сервера");
        }
    }

    function onTextareaChanged (event) {
        const contentEditable = event.target;
        contentEditable.style.height = 'auto';
        contentEditable.style.height = Math.min(contentEditable.scrollHeight, 167) + 'px';
    }

    useEffect(() => {
        getMovieById();
    }, [movieId]);

    if (movie == null){
        return(
            <h1> ничего нет </h1>
        )
    }

    else{
        const actors = movie.crew.filter((profession) => profession.slug == 'actor')
        const directors = movie.crew.filter((profession) => profession.slug == 'director')
        const producers = movie.crew.filter((profession) => profession.slug == 'producer')
        const screenwriters = movie.crew.filter((profession) => profession.slug == 'writer')
        const composers = movie.crew.filter((profession) => profession.slug == 'composer')
        const designers = movie.crew.filter((profession) => profession.slug == 'designer')
        const operators = movie.crew.filter((profession) => profession.slug == 'operator')
        const editors = movie.crew.filter((profession) => profession.slug == 'editor')

        const parsedDate = parseISO(movie.world_premier);
        const formattedDate = format(parsedDate, 'd MMMM yyyy', { locale: ru });

        let className="rathing-main"
        if (movie.rating >= 7.5){
            className += '-good';
        }

        else if (movie.rating >= 5.5 && movie.rating <= 7.5){
            className += '-average';
        }

        else{
            className += '-bad'
        }


        return(
            <div className="main-wrapper">
                <div className="wrapper">
                    <div className="wrapper-col-1">
                        <img className="poster-for-full-movie-info" src={movie.poster} alt={movie.name} />
                    </div>
    
                    <div className="wrapper-col-2">
                        <h1 className="title">{ movie.name }</h1>
                        <p className="description"> { movie.description }</p>
                        
                        <h2>О фильме</h2>
    
                        <ul className="params">
                            <li>
                                <span className="text-muted">Год производства</span>
                                <Link style={{textDecoration: "none", color:"black"}} to={`/movies/year/${movie.year}`}>{ movie.year }</Link>
                            </li>
                            
                            <li>
                                <span className="text-muted">Страна</span> 
                                <Link style={{textDecoration: "none", color:"black"}} to={`/movies/country/${movie.country}`}>{ movie.country }</Link>
                            </li>
                            
                            <li>
                                <span className="text-muted">Жанр</span>
                                <span>
                                    <div className="genre">
                                        {movie.genres.map((genre) => {
                                            return <div className="genre" key={genre.name}>
                                                        <Link style={{textDecoration: "none", color:"black"}} to={`/movies/genre/${genre.name}`}>{genre.name}&nbsp;</Link>
                                                    </div>
                                            })
                                        }
                                    </div>
                                </span>
                            </li>
                            
                            <li>
                                <span className="text-muted">Слоган</span>
                                <span className="tag">{ movie.tagline }</span>
                            </li>
                            
                            <li>
                                <span className="text-muted">Режиссёр</span>
                                <span> 
                                    <div className="persons">
                                        {directors.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {directors.length === 0 && <span>-</span>}
                                    </div> 
                                </span>
                            </li>

                            <li>
                                <span className="text-muted">Продюссер</span>
                                <span> 
                                    <div className="persons">
                                        {producers.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {producers.length === 0 && <span>-</span>}
                                    </div> 
                                </span>
                            </li>

                            <li>
                                <span className="text-muted">Сценарист</span>
                                <span> 
                                    <div className="persons">
                                        {screenwriters.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {screenwriters.length === 0 && <span>-</span>}
                                    </div> 
                                </span>
                            </li>

                            <li>
                                <span className="text-muted">Художник</span>
                                <span> 
                                    <div className="persons">
                                        {designers.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {designers.length === 0 && <span>-</span>}
                                    </div> 
                                </span>
                            </li>

                            <li>
                                <span className="text-muted">Композитор</span>
                                <span> 
                                    <div className="persons">
                                        {composers.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {composers.length === 0 && <span>-</span>}
                                    </div> 
                                </span>
                            </li>

                            <li>
                                <span className="text-muted">Монтажер</span>
                                <span> 
                                    <div className="persons">
                                        {editors.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {editors.length === 0 && <span>-</span>}
                                    </div> 
                                </span>
                            </li>

                            <li>
                                <span className="text-muted">Оператор</span>
                                <span> 
                                    <div className="persons">
                                        {operators.map((profession) => {
                                            return <div key={profession.person.id}>
                                                <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>{profession.person.name ? profession.person.name : profession.person.en_name}</Link>
                                            </div>
                                            })
                                        } {operators.length === 0 && <span></span>}
                                    </div> 
                                </span>
                            </li>
                            
                            <li>
                                <span className="text-muted">Время</span>
                                <time className="text-muted"> { movie.watch_time } мин. /&nbsp;{Math.floor(movie.watch_time/60)}:{movie.watch_time%60} </time>
                            </li>
                            
                            <li>
                                <span className="text-muted">Премьера в мире</span>
                                <time className="text-muted"> { formattedDate } </time>
                            </li>
                        </ul>
                    </div>
    
                    <div className="wrapper-col-3">
                        <div style={{display:"flex", flexDirection:"row", minWidth:"180px"}}>
                            <div className={className}> {movie.rating} </div> 
                            <span className="full-movie-rating-counts">{movie.annotated_count_rate} оценок</span>
                        </div>
                        <div className='my-own-rating-full-movie'>
                            {selectedRating && (
                                <div className="rate-movie-block">
                                    <button className="remove-movie-rate" 
                                        onClick={() => handleRatingClick(movie.id, null)}>Удалить оценку</button>
                                    <div className={`selected-user-rating ${getRatingColor(selectedRating)}`}> 
                                        {selectedRating} 
                                    </div>
                                </div>
                                
                            )}
                            {!selectedRating && !showRatingOptions && (
                                <button className="movie-by-id-set-rate" onClick={handleButtonClick}>
                                    Оценить фильм    
                                </button>
                            )}
                                

                            {showRatingOptions && !selectedRating &&(
                            <div ref={choicesRef} className='choices-for-marks-full-movie'>
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
                                        className={`rating-digit-full-movie ${colorClass} ${selectedRating === rating ? 'selected' : ''}`}
                                        onClick={() => handleRatingClick(movie.id ,rating)}> {rating} </span>
                                );
                                })}
                            </div>
                        )}
                        </div>
                        <a href="#" className="rathing-details">{movie.annotated_count_review}&nbsp;Рецензий</a>
                        <div style={{fontWeight: "bold", marginTop:"10px"}}>Актеры</div>
                        <div className="persons-actors">
                            {actors.map((profession) => (
                                <div key={profession.person.id}
                                    className="actor-wrapper"
                                >
                                    <Link to={`/person/${profession.person.id}`} style={{textDecoration: "none", color:"black"}}>
                                        {profession.person.name ? profession.person.name : profession.person.en_name}
                                    </Link>
                                    {profession.image && (
                                        <div className="actor-image-container">
                                            <img src={profession.image} alt={profession.person.name} />
                                        </div>
                                    )}
                                </div>
                            ))}
                            {actors.length === 0 && <span>-</span>}
                        </div>
                    </div>
                </div>
                <div className="movies-reviews-for-full-page">
                    <div className="input-module-for-movie-review">
                        <textarea  type="text" placeholder="Введите ваш комментарий" 
                            autoComplete="off" className="movie-review-input"
                            onChange={(event) => {setInputMessage(event.target.value); onTextareaChanged(event)}}
                            value={inputMessage}
                        />
                        <button className="btn-send-movie-review" onClick={()=>sendReview()}>Опубликовать</button>
                    </div>
                    
                    <div className="list-reviews">
                    {movie.movies_reviews.length > 0 ? (
                        movie.movies_reviews.map((review, index) => {
                        return (
                            review.review !== null && (
                            <div className="reviews-texts" key={index}>
                                <div className="movie-review-owner">
                                <img
                                    src={review.user.image}
                                    className="user-image-container"
                                    alt="User"
                                    width="40"
                                    height="40"
                                />
                                {review.user.username}
                                {review.user.is_critic && (
                                    <img src={CriticImage} width="80" height="30" />
                                )}
                                </div>
                                {review.review}
                            </div>
                            )
                        );
                        })
                    ) : (
                        <div className="no-reviews-text">Еще нет отзывов</div>
                    )}
                    </div>
                </div>
            </div> 
        )
    }
}

export default MovieById;