import { useState, useEffect, useContext } from 'react'
import axios from 'axios'
import MovieList from '../../components/movie-list/movie-list';
import Pagination from '../../components/pagination-page/pagination-page';
import { UserContext } from '../../context/user.context';
import FilterSelect from '../../components/select/select';
import { useParams } from 'react-router-dom';
import './movies.css'

const pageSize = 50;

function Movies() {
  const params = useParams();
  const genre = params.genre ? params.genre : "";
  const country = params.country ? params.country : "";
  const year = params.year ? params.year : "";

  const [page, setPage] = useState(1)
  const [numberOfPages, setNumberOfPages] = useState(1)
  const [selectedGenre, setSelectedGenre] = useState(genre)
  const [selectedYear, setSelectedYear] = useState(year)
  const [selectedCountry, setSelectedCountry] = useState(country)
  const [orderingField, setOrderingField] = useState("")
  const [filteredMovies, setFilteredMovies] = useState([])
  
  const { token } = useContext(UserContext) 

  const yearOption = [
    { value: "", label: 'Все года' },
    { value: 2023, label: '2023' },
    { value: 2022, label: '2022' },
    { value: 2021, label: '2021' },
    { value: 2020, label: '2020' },
  ];

  const sortFieldOption = [
    { value: "id", label: 'По порядку' },
    { value: "name", label: 'По названию' },
    { value: "rating", label: 'По рейтингу' },
    { value: "annotated_count_rate", label: 'По количеству оценок' },
  ];

  const genreOption = [
    { value: "", label: 'Все жанры' },
    { value: "драма", label: 'Драма' },
    { value: "боевик", label: 'Боевик' },
    { value: "комедия", label: 'Комедия' },
  ];

  const countryOption = [
    { value: "", label: 'Все страны' },
    { value: "США", label: 'США' },
    { value: "СССР", label: 'СССР' },
    { value: "Россия", label: 'Россия' },
    { value: "Великобритания", label: 'Великобритания' },
  ];

  async function getMovies(){
    let config = {
      headers: {
        "X-API-KEY": "3W0ZPKY-H5XM7X8-KRB88NB-QSF7VJ5",
      },
    };
    try {
      for (var k = 130; k < 130; k++){
        console.log("Начинаю получать фильмы с " + k + " страницы");
        const response = await axios.get(
          "https://api.kinopoisk.dev/v1.4/movie?page=" + k + "&limit=50&selectFields=id&selectFields=name&selectFields=names&selectFields=description&selectFields=slogan&selectFields=type&selectFields=year&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=premiere&notNullFields=id&notNullFields=name&notNullFields=description&notNullFields=slogan&notNullFields=type&notNullFields=year&notNullFields=movieLength&notNullFields=genres.name&notNullFields=countries.name&notNullFields=poster.url&notNullFields=persons.id&notNullFields=persons.name&notNullFields=persons.enName&notNullFields=persons.photo&notNullFields=persons.profession&notNullFields=persons.enProfession&notNullFields=premiere.world&type=movie",
          config
        );
        console.log(response.data.docs);
        for (var i = 0; i < 50; i++){
          console.log("Отправляю " + i + "фильм")
          await postMovie(response.data.docs[i])
          console.log("Загрузил " + i + "фильм")
        }
      }

      // const response = await axios.get(
      //       "https://api.kinopoisk.dev/v1.4/movie?page=1&limit=20&selectFields=id&selectFields=name&selectFields=names&selectFields=description&selectFields=slogan&selectFields=type&selectFields=year&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&selectFields=premiere&notNullFields=id&notNullFields=name&notNullFields=description&notNullFields=slogan&notNullFields=type&notNullFields=year&notNullFields=movieLength&notNullFields=genres.name&notNullFields=countries.name&notNullFields=poster.url&notNullFields=persons.id&notNullFields=persons.name&notNullFields=persons.enName&notNullFields=persons.photo&notNullFields=persons.profession&notNullFields=persons.enProfession&notNullFields=premiere.world&type=movie",
      //       config
      //     );
      //     for (var i = 0; i < 20; i++){
      //         console.log("Отправляю " + i + "фильм")
      //         await postMovie(response.data.docs[i])
      //         console.log("Загрузил " + i + "фильм")
      //     }
      } catch (error) {
      alert(error.message);
    }
  }

  async function postMovie(movie) {
    let data = {
      movies: movie,
    };
    let config = {
      headers: {
        Authorization: "Token " + token,
      },
    };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/movie/addMovies/",
        data,
        config
      );
      console.log(response.status);
    } catch (error) {
      alert(error.message);
    }
  }
  
  function next(){
    setPage(page + 1);
  }

  async function filterMovie() {
    let config = {}
    if (token && token.length > 4){
      config.headers = {
        Authorization: "Token " + token,
      };
    }
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/movie_short/?page=${page}&country=${selectedCountry}&year=${selectedYear}&genres__name=${selectedGenre}`,
        config
      );
      let movies = await response.data.results;
      let count =  await response.data.count;
      let res = Math.ceil(count / pageSize)
      setNumberOfPages(res);
      setFilteredMovies(movies)
    } catch (error) {
      alert(error.message);
    }
  }

  function sortMovie(){
    const result = [...filteredMovies];
    result.sort((a, b) => {
      const valueA = a[orderingField];
      const valueB = b[orderingField];

      switch (orderingField){
        case 'id':
          return valueA - valueB;
        case 'name':
          return valueA.localeCompare(valueB);
        case 'rating':
          return valueB - valueA;
        case 'annotated_count_rate':
          return valueB - valueA;
      }});
    setFilteredMovies(result);
  }

  useEffect(()=>{
    if (genre){
      setSelectedGenre(genre);
    }
    if (country){
      setSelectedCountry(country);
    }
    if(year){
      setSelectedYear(year);
    }
    filterMovie();
  }, [selectedGenre, selectedYear, selectedCountry, page, token]);

  useEffect(()=>{
    sortMovie();
  }, [orderingField, page]);

  const handleChangeYear = (selectedOption) => {
    setSelectedYear(selectedOption.value);
    setPage(1);
  };

  const handleChangeSortField = (selectedOption) => {
    setOrderingField(selectedOption.value);
  };

  const handleChangeGenreField = (selectedOption) => {
    setSelectedGenre(selectedOption.value);
    setPage(1);
  };

  const handleChangeCountryField = (selectedOption) => {
    setSelectedCountry(selectedOption.value);
    setPage(1);
  };

  return (
    <div className='main-wrapper'>
      <div className='movies-columns'>
        <div>
          <Pagination setPage={setPage} page={page} numberOfPages={numberOfPages}/>
          <MovieList className='movies-list' movies={filteredMovies} page={page} pageSize={pageSize}/> 
        </div>
        <div className='selects-for-sorting-filtering'>
          <FilterSelect
              options={sortFieldOption}
              defaultValue={sortFieldOption[0]}
              onChange={handleChangeSortField}
            />
            <FilterSelect
              options={genreOption}
              defaultValue={genre ? genreOption.find(option => option.value === genre) : genreOption[0]}
              onChange={handleChangeGenreField}
            />
            <FilterSelect
              options={countryOption}
              defaultValue={country ? countryOption.find(option => option.value === country) : countryOption[0]}
              onChange={handleChangeCountryField}
            />
            <FilterSelect
              options={yearOption}
              defaultValue={year ? yearOption.find(option => option.value === Number(year)) : yearOption[0]}
              onChange={handleChangeYear}
            />
        </div>
      </div>
    </div>
  )
}

export default Movies;