import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import axios from "axios";
import { format, parseISO } from 'date-fns';
import { ru } from 'date-fns/locale';

import './movie-by-id.styles.css'

const MovieById = () => {
    const[movie, setMovie] = useState(null)
    //const[movieId, setMovieId] = useState(12)    

    const params = useParams();
    let movieId = params.id;
    
    
    async function getMovieById(){
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/movie/${movieId}`
          );
          let movie = await response.data;
          console.log(response.data)
          setMovie(movie);
        } catch (error) {
          alert("ошибка в получении данных с сервера");
        }
      }

    useEffect(() => {
        console.log("юз эффект");
        //setMovieId(params.id);
        getMovieById();
    }, [movieId]);

    if (movie == null){
        return(
            <h1> ничего нет </h1>
        )
    }

    else{
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
                        <img src={movie.poster} alt={movie.name} />
                    </div>
    
                    <div className="wrapper-col-2">
                        <h1 className="title">{ movie.name }</h1>
                        <p className="description"> { movie.description }</p>
                        
                        <h2>О фильме</h2>
    
                        <ul className="params">
                            <li>
                                <span className="text-muted">Год производства</span>
                                { movie.year }
                            </li>
                            
                            <li>
                                <span className="text-muted">Страна</span> { movie.country }
                            </li>
                            
                            <li>
                                <span className="text-muted">Жанр</span>
                                <span>
                                    <div className="genre">
                                        {movie.genres.map((genre) => {
                                            return <div className="genre" key={genre.name}><a>{genre.name}&nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                                            return <div key={profession.person.id}><a>{profession.person.name} &nbsp;</a></div>
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
                        <div className={className}> {movie.rating} </div> 
                        <span className="rathing-counts">{movie.annotated_count_rate}</span>
                        <a href="#" className="rathing-details">459 рецензий</a>
                    </div>
                </div>
            </div> 
        )
    }
}

export default MovieById;