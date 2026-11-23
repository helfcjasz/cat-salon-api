import { useEffect, useState } from 'react';
import Header from './components/Header.jsx';
import VisitTable from './components/VisitTable.jsx';
import VisitForm from './components/VisitForm.jsx';
import './css/style.css';
import Footer from './components/Footer.jsx'
import Links from './components/Links.jsx'
import About from './components/About.jsx';
import Info from './components/Info.jsx';


const API_URL = '/api/items';


function App() {
  const [visits, setVisits] = useState([]);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    async function loadVisits() {
      try {
        const res = await fetch(API_URL);
        if (!res.ok) {
          throw new Error('Не вдалося завантажити записи з сервера');
        }
        const data = await res.json();
        setVisits(data);
      } catch (err) {
        setApiError(err.message);
      }
    }
    loadVisits();
  }, []);


  async function addVisit(visit) {
    setApiError('');
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...visit,
          catMass: Number(visit.catMass),
        }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || 'Помилка при збереженні запису');
      }
      const created = await res.json();
      setVisits((prev) => [...prev, created]);
    } catch (err) {
      setApiError(err.message);
    }
  }


  async function deleteVisit(id) {
    setApiError('');
    try{
      const res = await fetch(`${API_URL}/${id}`, {method: 'DELETE'});
      if(!res.ok){
        throw new Error('');
      }
      setVisits((prev) => prev.filter((visit) => visit.id !== id));
    } catch (err){
      setApiError(err.message);
    }
  }

  


  return (
    <>{}
    <Header />
    
    <div className="container">
      <About />
      <Info />
      {apiError && <p className="error">{apiError}</p>}
        {visits.length === 0 ? (
          <h2 className="section section-title empty-table">Записів немає</h2>
        ) : (
          <VisitTable visits={visits} onDelete={deleteVisit} />
        )}
      <VisitForm onAdd={addVisit} visits={visits}/>
      <Links />  
    </div>

    <Footer />

    </>
  );
}

export default App;
