import LittleMovieCard from '../movie-little-card/movie-little-card';

import { format, parseISO } from 'date-fns';
import { ru } from 'date-fns/locale';

import './person-by-id.css';
import { Link } from 'react-router-dom';

const PersonById = ({ personData }) => {

  const parsedDate = parseISO(personData.birth_day);
  const formattedDate = format(parsedDate, 'd MMMM yyyy', { locale: ru });

  const renderMoviesByProfessions = () => {
    const moviesByProfessions = {};
  
    personData.professions.forEach((profession) => {
      const professionName = getProfessionName(profession.slug);
  
      if (!moviesByProfessions[professionName]) {
        moviesByProfessions[professionName] = [];
      }
  
      moviesByProfessions[professionName].push(profession.movie);
    });
  
    return Object.keys(moviesByProfessions).map((professionName) => (
      <div key={professionName}>
        <h3>{professionName}</h3>
        <div className='movies-by-profession-by-person'>
          {moviesByProfessions[professionName].map((movie) => (
            <LittleMovieCard key={movie.id} movie={movie}/>
          ))}
        </div>
      </div>
    ));
  };
  
  const getProfessionName = (slug) => {
    const professionNames = {
      'actor': 'Актер',
      'director': 'Режиссер',
      'writer': 'Сценарист',
      'producer': 'Продюссер',
      'composer': 'Композитор',
      'operator': 'Оператор',
      'designer': 'Художник',
      'editor': 'Монтажер',
    };
  
    return professionNames[slug] || slug; // Возвращаем имя или сам slug, если нет соответствия
  };

  const renderBestMovies = () => {
    const uniqueMovies = {};
    const bestMovies = [];

    // Перебираем профессии
    personData.professions.forEach((profession) => {
      const movie = profession.movie;

      // Если фильм еще не добавлен или его рейтинг выше, добавляем в список лучших фильмов
      if (!uniqueMovies[movie.id] || uniqueMovies[movie.id].rating < movie.rating) {
        uniqueMovies[movie.id] = movie;
      }
    });

    // Выбираем первые 5 уникальных фильмов
    let count = 0;
    for (const movieId in uniqueMovies) {
      if (count < 5) {
        bestMovies.push(uniqueMovies[movieId]);
        count++;
      } else {
        break;
      }
    }

    return (
      <div style={{display:"flex", flexDirection:"column", gap:"10px"}}>
        <h3>Лучшие фильмы</h3>
        {Object.values(bestMovies).map((movie) => (
          <Link to={`/movies/${movie.id}`} style={{textDecoration: "none", color:"black"}} key={movie.id}>
            {movie.name} ({movie.year})
          </Link>
        ))}
      </div>
    );
  };

  return (
    <div className="person-page">
      <div className="person-wrapper-col-1">
        <img src={personData.photo} alt={personData.name} />
      </div>

      <div className="person-wrapper-col-2">
        <h1 className='title-for-person'>{personData.name}</h1>
        <p className='subtitle-for-person'>{personData.en_name}</p>
        <p>Дата рождения: {formattedDate}</p>
        {personData.death_day && <p>Died: {personData.death_day}</p>}
      </div>

      <div className="person-wrapper-col-3">
        {renderBestMovies()}
      </div>

      <div className="person-professions">
        {renderMoviesByProfessions()}
      </div>
    </div>
  );
};

export default PersonById;
