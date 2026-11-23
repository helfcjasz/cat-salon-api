function VisitRow({ visit, onDelete }) {
  return (
    <tr>
      <td>{visit.catName}</td>
      <td>{visit.catBreed}</td>
      <td>{visit.serviceType}</td>
      <td>{visit.serviceDate}</td>
      <td>{visit.serviceTime}</td>
      <td>{visit.catMass}</td>
      <td>{visit.agr_confirmation ? 'так' : 'ні'}</td>
      <td><button className="btn" onClick={() => onDelete(visit.id)}>Видалити</button></td>
    </tr>
  );
}

export default VisitRow;
