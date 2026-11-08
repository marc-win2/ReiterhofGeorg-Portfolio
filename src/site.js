document.documentElement.classList.add('js');
const menu = document.querySelector('.menu-button');
const nav = document.querySelector('#navigation');
function closeMenu(returnFocus = false) {
  nav.classList.remove('open');
  menu.setAttribute('aria-expanded', 'false');
  menu.textContent = 'Menü ☰';
  if (returnFocus) menu.focus();
}
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  nav.classList.toggle('open', open);
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? 'Schließen ×' : 'Menü ☰';
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && nav.classList.contains('open')) closeMenu(true);
});
document.addEventListener('click', event => {
  if (!event.target.closest('.header')) closeMenu();
});
matchMedia('(min-width: 801px)').addEventListener('change', () => closeMenu());
