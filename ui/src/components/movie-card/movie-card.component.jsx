import { Link } from 'react-router-dom';
import { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import './movie-card.styles.css'
import Modal from '../modal/modal.component';
import LoginForm from '../login-form/login-form.component';

import { UserContext } from '../../context/user.context';

const MovieCard = ({ movie, index }) => {
    const [selectedRating, setSelectedRating] = useState(movie.user_rating);
    const [showRatingOptions, setShowRatingOptions] = useState(false);
    const { token } = useContext(UserContext)
    const [active, setActive] = useState(false);

    async function testUpdateRate (id, rating) {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'rate': rating,
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
        console.log(rating);
        testUpdateRate(id, rating);
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
        <div className={movie.user_is_watched ? 'movie-card watched' : 'movie-card'}>
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
                <button className="movie-card-additional-options"/>
            </div>
            <Modal active={active} setActive={setActive}>
                <LoginForm />
            </Modal>
        </div>
        
    );
  };
  
  export default MovieCard;