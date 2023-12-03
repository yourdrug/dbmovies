import Movies from './routes/movies/movies.component'
import Navigation from './routes/navigation/navigation.component'
import Profile from './routes/profile/profile.component'
import Home from './routes/home/home.component'
import {Routes, Route} from 'react-router-dom'

import './App.css'
import MovieById from './components/movie-by-id/movie-by-id.component'

function App() {

  return (
    <Routes>
      <Route path='/' element={<Navigation/>}>
        <Route index element={<Home/>}/>
        <Route path='movies' element={<Movies/>}/>
        <Route path='movies/:id' element={<MovieById/>}/>
        <Route path='profile' element={<Profile/>}/>
      </Route>
    </Routes>
  )
}

export default App;
