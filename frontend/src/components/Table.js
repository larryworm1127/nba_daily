import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

const Table = ({data}) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="container stats-table-extended">

      <table className="team-list-table table table-sm text-lg-center">
        <thead className="thead-inverse">
          <tr className="bg-primary text-white">
            {Object.entries(data[0]).map(el => <th className="bg-primary" key={key(el)}>{el[0]}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              {Object.entries(el).map(el => <td key={key(el)}>{el[1]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
Table.propTypes = {
  data: PropTypes.array.isRequired
};
export default Table;