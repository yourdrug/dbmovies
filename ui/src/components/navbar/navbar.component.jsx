import { Link } from 'react-router-dom';
import Modal from '../modal/modal.component';
import LoginForm from '../login-form/login-form.component';
import SignUpForm from '../signup-form/signup-form.component';
import './navbar.styles.css';
import { useState, useContext } from 'react';

import axios from 'axios';

import { UserContext } from '../../context/user.context';

const Navbar = () => {
    const [active, setActive] = useState(false);
    const [searchInfo, setSearchInfo] = useState(null);
    const [searchInfoClass, setSearchInfoClass] = useState('search-info');

    const handleSearchFocus = () => {
        setSearchInfoClass('search-info-active');
        handleDebouncedInputChange("");
    };

    const handleSearchBlur = () => {
        // Добавляем небольшую задержку перед скрытием
        setTimeout(() => {
            setSearchInfoClass('search-info');
        }, 200);
    }

    
    const { currentUser } = useContext(UserContext);  
    
    const handleDebouncedInputChange = async (value) => {
        try {
            const response = await axios.get(
              `http://127.0.0.1:8000/search/?query=${value}`
            );
            setSearchInfo(response.data);
            console.log(response.data)
          } catch (error) {
            alert("ошибка в получении данных с сервера");
          }
      };
    
    async function onChangeInputHandler(event){
        const value = event.target.value;
        setTimeout(async () => {
            await handleDebouncedInputChange(value);
          }, 1000);
    }

    return(
        <div className="navbar">
            <Link className="appName" to='/' style={{ textDecoration: 'none' }}>Название</Link> 
            <input className='search-box' type='searchbox' placeholder='Поиск по всему сайту'
                    onChange={(event) => onChangeInputHandler(event)} onFocus={() => handleSearchFocus()}
                    onBlur={() => handleSearchBlur()}/>
            {searchInfo && (
                <div className={searchInfoClass}>
                    {searchInfo.results_movie && searchInfo.results_movie.length > 0 && (
                        <div className='searched-movies'>
                            <span className='text-muted-for-navbar'>Фильмы</span>
                            {searchInfo.results_movie.map((movie) => (
                                <Link key={movie.id} to={`/movies/${movie.id}`} style={{textDecoration: "none", color:"black"}}>
                                    <div className='movie-card-for-seacrh-bar'>
                                        <img className='img-for-search-bar' src={movie.poster}/>
                                        <div>
                                            <div style={{fontWeight:"bold"}}>{movie.name}</div>
                                            <div style={{display:"flex", flexDirection:"row", gap:"10px"}}>
                                                <div> {movie.country}, {movie.year} </div>
                                                <div style={{color: movie.rating < 5.5 ? 'red' : (movie.rating >= 5.5 && movie.rating <= 7.5 ? 'gray' : 'green'), fontWeight:"bold"}}>
                                                    {movie.rating}</div>
                                            </div>  
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    )}
                    {searchInfo.results_person && searchInfo.results_person.length > 0 && (
                        <div className='searched-persons'>
                            <span className='text-muted-for-navbar'>Персоны</span>
                            {searchInfo.results_person.map((person) => (
                                <Link key={person.id} to={`/person/${person.id}`} style={{textDecoration: "none", color:"black"}}>
                                <div className='movie-card-for-seacrh-bar'>
                                    <img className='img-for-search-bar' src={person.photo}/>
                                    <div>
                                        <div style={{fontWeight:"bold"}}>{person.name}</div>
                                        <div>{person.en_name}</div>
                                    </div>
                                </div>
                            </Link>
                            ))}
                        </div>
                    )}
                </div>
            )}           
            { !currentUser ? 
            (<div className='auth-module'>
                <a className="logbtn" onClick={() => setActive(true)}>Войти</a> 
                <Modal active={active} setActive={setActive}>
                    <SignUpForm/>
                </Modal>
            </div> 
            ) : (
            <div className='auth-module'>
                <div className='user-avatar'>
                    <img src={currentUser ? currentUser.image : ''} alt='NICHEGO NET'></img>
                </div>
                <Link className="navbar-username" to='/profile' style={{ textDecoration: 'none' }}>{currentUser.username}</Link>
            </div>) }    
        </div>
        
    )
}

export default Navbar;