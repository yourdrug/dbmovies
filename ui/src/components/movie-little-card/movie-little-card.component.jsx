import './movie-little-card.styles.css';
import { useState } from 'react';
import { debounce } from 'lodash';

const LittleMovieCard = ({movie}) => {
    const [isHovered, setIsHovered] = useState(false);

    const handleMouseEnter = debounce(() => {
        setIsHovered(true);
      }, 100); // Установите интервал debounce по вашему усмотрению
    
      const handleMouseLeave = debounce(() => {
        setIsHovered(false);
      }, 100);

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
        <div className='short-movie-card'>
            <span className='name-for-little-moviecard'> {movie.name} </span>
            <img src={movie.poster} width={200} height={300}></img>
                <div className='additional-info-for-little-card'>
                    <span className='country-and-year'>{movie.country}, {movie.year} </span> 
                    <div>
                        <span className={className}> {movie.rating}</span>
                        <span className='count-rates-for-little-card'>  {movie.annotated_count_rate !=0 && movie.annotated_count_rate} </span>
                    </div>
                </div>
        </div>
    );
};
  
export default LittleMovieCard;
