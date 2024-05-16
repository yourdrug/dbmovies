import { useEffect, useState, useContext } from "react";
import RandomMovie from "../../components/random-movie/random-movie";
import { UserContext } from "../../context/user.context";
import { toast } from "react-toastify";

import axios from "axios";

import './evening-movie.css'

const EveningMovie = () => {
    const [movie, setMovie] = useState(null)
    const [counter, setCounter] = useState(1)
    const { token } = useContext(UserContext)

    async function getMovie(){
        try {
          const response = await axios.get("http://127.0.0.1:8000/movie/randomMovie/");
          let info = await response.data;
          setMovie(info);
        } catch (error) {
            toast.warn("Технические неполадки. Попробуйте позже.");
        }
    }

    async function updateBookmarks () {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'in_bookmarks': true,
        };
        try {
            await axios.patch(`http://127.0.0.1:8000/movie_relation/${movie.id}/`, data, config);
            toast.success("Фильм добавлен в «Избранное»!") 
        } catch (error) {
            toast.warn("Технические неполадки. Попробуйте позже.");
        }
    }

    async function updateWillWatch () {
        let config = {
            headers: {
              Authorization: "Token " + token,
            },
        };
        let data = {
            'will_watch': true,
        };
        try {
            const response = await axios.patch(`http://127.0.0.1:8000/movie_relation/${movie.id}/`, data, config);
            toast.success("Фильм добавлен в альбом «Буду смотреть»!") 
        } catch (error) {
            toast.warn("Технические неполадки. Попробуйте позже.");
        }
    }

    useEffect(()=>{
        getMovie();
    }, [counter]);


    return (
        <div className="main-wrapper">
            <div style={{display:"flex", flexDirection:"row"}}>
                <button className="btn-for-next-random-movie" onClick={()=>updateWillWatch()}> Буду смотреть </button>
                <button className="btn-for-next-random-movie" onClick={()=>updateBookmarks()}> В избранное </button>
                <button className="btn-for-next-random-movie" onClick={()=>{setCounter(counter + 1);}}> Следующий! </button>
            </div>
            {movie && <RandomMovie movie={movie}/>}
        </div>
        
    );
  };
  
  export default EveningMovie;