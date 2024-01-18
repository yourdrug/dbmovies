import Movies from './routes/movies/movies'
import Navigation from './routes/navigation/navigation'
import Profile from './routes/profile/profile'
import Home from './routes/home/home'
import HomeScreen from './routes/chatting/chatting'
import AlbumMovies from './routes/album-movies/album-movies'
import EveningMovie from './routes/evening-movie/evening-movie'
import EditProfile from './routes/edit-profile/edit-profile'
import {Routes, Route} from 'react-router-dom'

import './App.css'
import MovieById from './components/movie-by-id/movie-by-id'
import PersonPage from './routes/person/person-page'

function App() {

  return (
    <Routes>
      <Route path='/' element={<Navigation/>}>
        <Route index element={<Home/>}/>
        <Route path='movies' element={<Movies/>}/>
        <Route path='movies/:id' element={<MovieById/>}/>
        <Route path='profile' element={<Profile/>}/>
        <Route path='chatting' element={<HomeScreen/>}/>
        <Route path='chatting/:chatId' element={<HomeScreen/>}/>
        <Route path='profile/:userId/:albumName' element={<AlbumMovies/>}/>
        <Route path='profile/edit' element={<EditProfile/>}/>
        <Route path='person/:id' element={<PersonPage/>}/>
        <Route path='random-movie' element={<EveningMovie/>}/>
      </Route>
    </Routes>
  )
}

export default App;
