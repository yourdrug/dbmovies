import MovieCard from '../movie-card/movie-card';
import './movie-list.css';



const MovieList = ({ movies, page, pageSize}) => (
  
  <div className='movie-list'>
    {movies.map((movie) => {
      return <MovieCard key={movie.id} movie={movie} index={movies.indexOf(movie) + 1 + (page - 1) * pageSize}/>;
    })}
  </div>
);

export default MovieList;