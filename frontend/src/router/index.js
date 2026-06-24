import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/catalog',
    redirect: { name: 'books' },
  },
  {
    path: '/books',
    component: () => import('@/views/BooksLayoutView.vue'),
    children: [
      {
        path: '',
        name: 'books',
        component: () => import('@/views/CatalogView.vue'),
      },
      {
        path: 'new',
        name: 'book-new',
        component: () => import('@/views/BookCreateView.vue'),
      },
      {
        path: ':id/edit',
        name: 'book-edit',
        component: () => import('@/views/BookEditView.vue'),
      },
    ],
  },
  {
    path: '/reader',
    name: 'reader',
    component: () => import('@/views/ReaderView.vue'),
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: () => import('@/views/FavoritesView.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});
