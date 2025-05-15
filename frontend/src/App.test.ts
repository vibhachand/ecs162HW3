import { test, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/svelte';
import App from './App.svelte';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import Article from './lib/Article.svelte';

test('App', async () => {
    render(App);
})
// references: https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector
// --- backend tests --- ALSO TESTED WITH PYTEST IN BACKEND FOLDER

// Set the API key for testing
process.env.NYT_API_KEY = 'api-key';

// Create the mock API server using MSW v2 syntax
const apiServer = setupServer(
  http.get('/api/key', () => {
    return HttpResponse.json({ apiKey: 'api-key' });
  })
);

// setup the testing server
beforeEach(() => {
  apiServer.listen();
});

// reset the testing server
afterEach(() => {
  apiServer.resetHandlers();
  apiServer.close();
});

// api key test
test('fetch correct api key', async () => {
  const res = await fetch('/api/key');
  const data = await res.json();

  expect(res.ok).toBe(true);
  expect(data).toHaveProperty('apiKey');
  expect(data.apiKey).toBe('api-key');
});

// --- frontend tests ---

// media queries tests
test('media queries test', async () => {
    // 3 column layout
    global.innerWidth = 1050;
    render(App);

    const cols = document.querySelectorAll('.grid-container .column1');
    expect(cols.length).toBe(2);

    // 2 column layout
    global.innerWidth = 850;
    window.dispatchEvent(new Event('resize'));
    await new Promise(resolve => setTimeout(resolve, 1000));

    const cols2 = document.querySelectorAll('.grid-container .column2');
    expect(cols2.length).toBe(2);

    // 1 column layout
    global.innerWidth = 400;
    window.dispatchEvent(new Event('resize'));
    await new Promise(resolve => setTimeout(resolve, 1000));

    const cols3 = document.querySelectorAll('.grid-container .column2');
    expect(cols3.length).toBe(2);
});

// test header loaded
test ('header loaded', () => {
    // header loaded
    const header = screen.getAllByRole('banner')
    expect(header).to.exist;
});

// test logo loaded
// test ('logo loaded', () => {
//     const { container } = render(App);
  
//     const logo = container.querySelector('img.logo');
    
//     expect(logo).to.exist;
//     expect(logo.src).to.include('images/The_New_York_Times_logo.png');  
// });

// test each article has expected content
test('each article has expected content', () => {
    // fake article data
    const article = {
      headline: 'headline',
      url: 'https://test.com',
      author: 'author',
      abstract: 'abstract',
      image: 'image.jpg',
      caption: 'caption'
    };
    
    const { container } = render(Article, {
      props: {
        id: 0,
        articles: [article],
      }
    });
    
    // testing if article has an image
    const images = container.querySelectorAll('img');
    expect(images.length).toBe(1);

    // testing if article has link
    const link = container.querySelector('a');
    expect(link).not.toBeNull();
    if (link){
      expect(link.href).toContain('https://test.com');
    }

    // testing if article has a headline
    const headline = container.querySelector('h2');
    expect(headline).not.toBeNull();
    expect(headline?.textContent).toContain('headline');

    // testing if article has an abstract
    const abstract = container.querySelector('[data-testid="article-abstract"]');
    if(abstract){
      expect(abstract?.textContent).toContain('abstract');
    }
    
    //testing if article has an author 
    const author = container.querySelector('[data-testid="article-author"]');
    if(author){
      expect(author?.textContent).toContain('author');
    }
    
  });