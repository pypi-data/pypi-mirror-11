//    This file is part of CVXcanon.
//
//    CVXcanon is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    CVXcanon is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with CVXcanon.  If not, see <http://www.gnu.org/licenses/>.

#include "CVXcanon.hpp"
#include <iostream>
#include <map>
#include "LinOp.hpp"
#include "LinOpOperations.hpp"
#include "ProblemData.hpp"

std::map<int, std::vector<Matrix> > mul_by_const(Matrix &coeff_mat,
        std::map<int, std::vector<Matrix> > &rh_coeffs,
        std::map<int, std::vector<Matrix> > &result) {

	typedef std::map<int, std::vector<Matrix> >::iterator it_type;
	for (it_type it = rh_coeffs.begin(); it != rh_coeffs.end(); ++it){
		int id = it->first;
		for (unsigned i = 0; i < it->second.size(); i++) {
			Matrix rh = it->second[i];
			if (coeff_mat.rows() == 1 && coeff_mat.cols() == 1) {
				double scalar = coeff_mat.coeffRef(0, 0);
				result[id].push_back(scalar * rh);
			} else {
				result[id].push_back( coeff_mat * rh );
			}
		}
	}
	return result;
}

std::map<int, std::vector<Matrix> > get_coefficient(LinOp &lin) {
	std::map<int, std::vector<Matrix> > coeffs;
	if (lin.type == VARIABLE) { 				// If a lin op is a variable, we hit one of our base cases
		std::map<int, Matrix> new_coeffs = get_variable_coeffs(lin);
		typedef std::map<int, Matrix >::iterator it_type;
		for(it_type it = new_coeffs.begin(); it != new_coeffs.end(); ++it){
			coeffs[it->first].push_back(it->second);
		}
	}
	else if ( lin.has_constant_type()) {								// If it is a constant, we hit our other base case
		std::map<int, Matrix> new_coeffs = get_const_coeffs(lin);	// id here will be CONSTANT_TYPE
		typedef std::map<int, Matrix >::iterator it_type;
		for(it_type it = new_coeffs.begin(); it != new_coeffs.end(); ++it){
			coeffs[it->first].push_back(it->second);
		}
	}
	else {
		std::vector<Matrix> coeff_mat = get_func_coeffs(lin); // The function coefficient by which we multiply the arguments
		for (unsigned i = 0; i < lin.args.size(); i++) {		 // in order
			Matrix coeff = coeff_mat[i];
			std::map<int, std::vector<Matrix> > rh_coeffs = get_coefficient(*lin.args[i]);
			std::map<int, std::vector< Matrix> > new_coeffs;
			mul_by_const(coeff, rh_coeffs, new_coeffs);

			typedef std::map<int, std::vector< Matrix> >::iterator it_type;
			for (it_type it = new_coeffs.begin(); it != new_coeffs.end(); ++it){
				coeffs[it->first].insert(coeffs[it->first].end(), it->second.begin(), 
																 it->second.end());
			}
		}
	}
	return coeffs;
}


int get_horiz_offset(int id, std::map<int, int> &offsets,
                     int &horiz_offset, LinOp &lin) {
	if ( !offsets.count(id) ) {
		offsets[id] = horiz_offset;
		horiz_offset += lin.size[0] * lin.size[1];
	}
	return offsets[id];
}



/* function: add_matrix_to_vectors
*
* This function adds a matrix to our sparse matrix triplet
* representation, by using eigen's sparse matrix iterator
* This function takes horizontal and vertical offset, which indicate
* the offset of this block within our larger matrix.
*/

void add_matrix_to_vectors(Matrix & block, std::vector<double> &V,
                           std::vector<int>  &I, std::vector<int> &J,
                           int vert_offset, int &horiz_offset) {
	for ( int k = 0; k < block.outerSize(); ++k ) {
		for ( Matrix::InnerIterator it(block, k); it; ++it ) {
			V.push_back(it.value());
			I.push_back(it.row() + vert_offset);   	// pushing back the current row index
			J.push_back(it.col() + horiz_offset);   // pushing back current column index
		}
	}
}

void extend_constant_vec(std::vector<double> &const_vec, int &vert_offset,
                         Matrix &block) {
	int rows = block.rows();
	for ( int k = 0; k < block.outerSize(); ++k ) {
		for ( Matrix::InnerIterator it(block, k); it; ++it ) {
			int idx = vert_offset + (it.col() * rows) + it.row();
			const_vec[idx] += it.value();
		}
	}
}

void process_constraint(LinOp & lin, std::vector<double> &V,
                        std::vector<int> &I, std::vector<int> &J,
                        std::vector<double> &constant_vec, int &vert_offset,
                        std::map<int, int> &id_to_col, int & horiz_offset) {
	std::map<int, std::vector<Matrix> > coeffs = get_coefficient(lin);	// Getting the coefficient for the current constraint

	typedef std::map<int, std::vector<Matrix> >::iterator it_type;
	for(it_type it = coeffs.begin(); it != coeffs.end(); ++it){
		int id = it->first;									// We determine the horiz offset by the id
		std::vector<Matrix> blocks = it->second;
		for (unsigned i = 0; i < blocks.size(); i++) {
			Matrix block = blocks[i];
			if ( id == CONSTANT_ID ) {							// If this LinOp is a we add these coefficients
				extend_constant_vec(constant_vec, vert_offset, block);	// to our constant vec.
			}
			else {
				int offset = get_horiz_offset(id, id_to_col, horiz_offset, lin);
				add_matrix_to_vectors(block, V, I, J, vert_offset, offset);
			}
		}
	}
}

int get_total_constraint_length(std::vector< LinOp* > constraints) {
	int result = 0;
	for (unsigned i = 0; i < constraints.size(); i++) {
		result += constraints[i]->size[0] * constraints[i]->size[1];
	}
	return result;
}

/* function: build_matrix
*
* Description: Given a list of linear operations, this function returns a data
* structure containing a sparse matrix representation of the
* second order cone problem of the problem.
*
* Input: std::vector<LinOp *> constraints, our list of constraints represented
* as a linear operation tree
*
* Output: prob_data, a data structure which contains a sparse representation
* of the coefficient matrix, a dense representation of the constant vector,
* and maps containing our mapping from variables, and a map from the rows of our
* matrix to their corresponding constraint.
*
*/

ProblemData build_matrix(std::vector< LinOp* > constraints,
                         std::map<int, int> id_to_col) {
	ProblemData prob_data;
	int num_rows = get_total_constraint_length(constraints);
	prob_data.const_vec = std::vector<double> (num_rows, 0);
	prob_data.id_to_col = id_to_col; 						// TODO: Make this more efficient
	int vert_offset = 0;
	int horiz_offset  = 0;
	for (unsigned i = 0; i < constraints.size(); i++) {		// Processing each constraint
		LinOp constr = *constraints[i];
		process_constraint(constr, prob_data.V, prob_data.I, prob_data.J,
		                   prob_data.const_vec, vert_offset,
		                   prob_data.id_to_col, horiz_offset);
		prob_data.const_to_row[i] = vert_offset;
		vert_offset += constr.size[0] * constr.size[1];
	}
	return prob_data;
}