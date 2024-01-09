import './movie-little-card.css';
import { Link } from "react-router-dom";

const LittleMovieCard = ({movie}) => {

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
        <Link className='link-for-little-card' to={`/movies/${movie.id}`} style={{textDecoration: "none"}}>
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
        </Link>
    );
};
  
export default LittleMovieCard;
