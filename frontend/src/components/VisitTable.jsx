import VisitRow from "./VisitRow.jsx";


function VisitTable({visits, onDelete}) {
    return (
        <section className="section">
        <h2 className="section-title">Записи на грумінг</h2>
            <div className="table-wrapper">
                <table className = "table">
                    <caption className="table-caption">Найближчі візити</caption>
                    <thead>
                        <tr>
                            <th>Кличка</th>
                            <th>Порода</th>
                            <th>Послуга</th>
                            <th>Дата візиту</th>
                            <th>Час візиту</th>
                            <th>Вага, кг</th>
                            <th>Агресивна тварина</th>
                            <th>Видалити</th>
                        </tr>
                    </thead>
                    <tbody>
                        {visits.map(visit => (
                            <VisitRow key={visit.id} visit = {visit} onDelete={onDelete}/>
                        ))}

                    </tbody>
                </table>
            </div>
        </section>
  );
}

export default VisitTable;
