import './movie-card.styles.css'

const MovieCard = ({ movie, index }) => {
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
        <div className="movie-card">
            <div className="number"> {index} </div>
            <div className="poster">
                <img src={movie.poster} />
            </div>
            <div className="movie-info">
                <div className="movie-name">{ movie.name }</div>
                <div className="movie-desc"> { movie.year }, { movie.watch_time.split("/")[0] } </div>
                <div className="movie-more-desc"> { movie.country.split(",")[0] } | { movie.genres[0].name }
                    &nbsp;Режиссёр: { movie.crew[1].person.name } <br />
                    <br /> В ролях: { movie.crew[2].person.name }, { movie.crew[3].person.name }</div>
            </div>
            <div className="additional-info">
                <div className={className}> {movie.rating} </div> 
                <div className="count-rates">{ movie.annotated_count_rate }</div>
            </div>
        </div>
    );
  };
  
  export default MovieCard;