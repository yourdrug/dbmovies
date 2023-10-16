import StartPage from "@/pages/StartPage";
import MoviesPage from "@/pages/MoviesPage";
import MovieIdPage from "@/pages/MovieIdPage";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: '/',
        component: StartPage
    },
    {
        path: '/movies',
        component: MoviesPage
    },
    {
        path: '/movies/:id',
        component: MovieIdPage
    },
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

export default router;