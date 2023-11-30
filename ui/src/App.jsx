import Films from './routes/films/films.component'
import Navigation from './routes/navigation/navigation.component'
import Home from './routes/home/home.component'
import {Routes, Route} from 'react-router-dom'

import './App.css'

function App() {

  return (
    <Routes>
      <Route path='/' element={<Navigation/>}>
        <Route index element={<Home/>}/>
        <Route path='films' element={<Films/>}/>
      </Route>
    </Routes>
  )
}

export default App;
