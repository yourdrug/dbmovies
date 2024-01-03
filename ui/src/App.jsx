import Movies from './routes/movies/movies.component'
import Navigation from './routes/navigation/navigation.component'
import Profile from './routes/profile/profile.component'
import Home from './routes/home/home.component'
import HomeScreen from './routes/chatting/chatting.component'
import AlbumMovies from './routes/album-movies/album-movies.component'
import {Routes, Route} from 'react-router-dom'

import './App.css'
import MovieById from './components/movie-by-id/movie-by-id.component'
import PersonPage from './routes/person/person-page.component'

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
        <Route path='person/:id' element={<PersonPage/>}/>
      </Route>
    </Routes>
  )
}

export default App;
