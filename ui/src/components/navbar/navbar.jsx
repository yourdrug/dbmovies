import { Link } from 'react-router-dom';
import Modal from '../modal/modal';
import LoginForm from '../login-form/login-form';

import GlobalChat from '../global-chat/global-chat';

import './navbar.css';
import { useState, useContext, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';

import axios from 'axios';

import { UserContext } from '../../context/user.context';

function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);
  
    useEffect(() => {
      const handler = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);
  
      return () => {
        clearTimeout(handler);
      };
    }, [value, delay]);
  
    return debouncedValue;
  }

const Navbar = () => {
    const [active, setActive] = useState(false);
    const [globalChatActive, setGlobalChatActive] = useState(false);
    const [inputInfo, setInputInfo] = useState("")
    const [searchInfo, setSearchInfo] = useState(null);
    const [searchInfoClass, setSearchInfoClass] = useState('search-info');

    const { currentUser, setSocket } = useContext(UserContext); 

    const debouncedSearchTerm = useDebounce(inputInfo, 500)

    useEffect(() => {
        if (currentUser){
            let socket = new WebSocket(`ws://127.0.0.1:8000/ws/users/${currentUser.id}/chat/`);
            setSocket(socket);
        }

        else{
            let socket = new WebSocket('ws://127.0.0.1:8000/ws/guest/');
            setSocket(socket);
        }
    }, [currentUser]);


    const handleDebouncedInputChange = async (value) => {
        try {
            const response = await axios.get(
              `http://127.0.0.1:8000/search/?query=${value}`
            );
            setSearchInfo(response.data);
          } catch (error) {
            toast.warn("Технические неполадки, попробуйте позже.")
          }
    };

    useEffect(() => {
        handleDebouncedInputChange(inputInfo);
    }, [debouncedSearchTerm]);

    const handleSearchFocus = () => {
        setSearchInfoClass('search-info-active');
        handleDebouncedInputChange(inputInfo);
    };

    const handleSearchBlur = () => {
        // Добавляем небольшую задержку перед скрытием
        setTimeout(() => {
            setSearchInfoClass('search-info');
        }, 200);
    }
    
    
    
    return(
        <div className="navbar">
            <ToastContainer className="my-toast-container"
                position="bottom-right"
                autoClose={5000}
                limit={10}
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                rtl={false}
                pauseOnFocusLoss={false}
                draggable={false}
                pauseOnHover={false}
                theme="light"
            />
            <Link className="appName" to='/' style={{ textDecoration: 'none' }}>Название</Link> 
            <input className='search-box' type='searchbox' placeholder='Поиск по всему сайту' value={inputInfo}
                    onChange={(event) => setInputInfo(event.target.value)} onFocus={() => handleSearchFocus()}
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
                    {searchInfo.results_person.length == 0 && searchInfo.results_movie.length == 0 && (
                        <div className='nothing-found'>
                            Ничего не найдено 
                        </div>
                    )}
                </div>
            )}   
            { !currentUser ? 
            (<div className='auth-module'>
                <a className="logbtn" onClick={() => setActive(true)}>Войти</a> 
                <Modal active={active} setActive={setActive}>
                    <LoginForm setActive={setActive}/>
                </Modal>
            </div> 
            ) : (
            <div className='auth-module'>
                <div className='user-avatar-in-navbar'>
                    <img src={currentUser ? currentUser.image : ''} alt={currentUser.username}></img>
                </div>
                <Link className="navbar-username" to='/profile' style={{ textDecoration: 'none' }}>{currentUser.username}</Link>
            </div>) } 
            <GlobalChat active={globalChatActive} setActive={setGlobalChatActive}></GlobalChat>
        </div>
        
    )
}

export default Navbar;