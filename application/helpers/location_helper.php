<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'get_loc_by_zipcode' )) {
	/**
	 * Get the location related information by zipcode
	 *
	 * @param string $zipcode        	
	 * @return The location array containing region and geometry information
	 */
	function get_loc_by_zipcode($zipcode) {
		$CI = & get_instance ();
		$CI->db->where ( 'zipcode', $zipcode );
		$query = $CI->db->get ( 'cache_zipcode' );
		$zipcode_row = $query->row_array ();
		if ($zipcode_row) {
			return $zipcode_row;
		}
		
		// Retreive the zipcode information from the google api
		$ch = curl_init (); // initiate curl
		$key = $CI->config->config ['google_apis'] ['key'];
		$url = "https://maps.googleapis.com/maps/api/geocode/json?address=&components=postal_code:$zipcode&key=$key";
		curl_setopt ( $ch, CURLOPT_URL, $url );
		curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true ); // return the output in string format
		$zipcod_json = curl_exec ( $ch ); // execute
		if (curl_errno ( $ch )) {
			log_message ( 'error', 'Faild to call google api: ' . print_r ( curl_getinfo ( $ch ), TRUE ) );
			curl_close ( $ch ); // close curl handle
			return FALSE;
		}
		curl_close ( $ch ); // close curl handle
		
		$zipcod_info = json_decode ( $zipcod_json, true );
		if (! $zipcod_info) {
			log_message ( 'error', 'Faild to parse the google api response: ' . print_r ( $zipcod_json, TRUE ) );
			return FALSE;
		}
		
		$status = array_key_exists ( 'status', $zipcod_info ) ? $zipcod_info ['status'] : 'UNKNOWN';
		if ($status != "OK") {
			log_message ( 'error', "The status in the google api response is not OK: $status" );
			return FALSE;
		}
		
		// build zipcode information
		$zipcode_data = array (
				'zipcode' => $zipcode,
				'raw_data' => $zipcod_json 
		);
		
		$location = isset ( $zipcod_info ['results'] [0] ['geometry'] ['location'] ) ? $zipcod_info ['results'] [0] ['geometry'] ['location'] : NULL;
		if ($location) {
			$zipcode_data ['latitude'] = $location ['lat'];
			$zipcode_data ['longitude'] = $location ['lng'];
		}
		
		$address_components = isset ( $zipcod_info ['results'] [0] ['address_components'] ) ? $zipcod_info ['results'] [0] ['address_components'] : NULL;
		if ($address_components) {
			$need_types = array (
					'country',
					'administrative_area_level_1',
					'administrative_area_level_2',
					'locality',
					'sublocality_level_1' 
			);
			foreach ( $address_components as $address_component ) {
				$type = $address_component ['types'] [0];
				if (in_array ( $type, $need_types )) {
					$zipcode_data [$type] = $address_component ['long_name'];
					$zipcode_data ["${type}_s"] = $address_component ['short_name'];
				}
			}
		}
		
		// insert the data into DB
		$CI->db->insert ( 'cache_zipcode', $zipcode_data );
		if ($CI->db->_error_number ())
			log_message ( 'error', 'get_loc_by_zipcode: ' . $CI->db->_error_number () . ':' . $CI->db->_error_message () );
		
		return $zipcode_data;
	}
}

if (! function_exists ( 'get_loc_by_latlng' )) {
	/**
	 *
	 * Get the location related information by latitude & longitude
	 *
	 * @param float $latitude        	
	 * @param float $longitude        	
	 * @return The location array containing region and geometry information
	 */
	function get_loc_by_latlng($latitude, $longitude) {
		$CI = & get_instance ();
		$range = calculate_latitude_longitude_range ( $latitude, $longitude, 5 );
		$CI->db->where ( 'latitude > ', $range ['latitude_min'] );
		$CI->db->where ( 'latitude < ', $range ['latitude_max'] );
		$CI->db->where ( 'longitude > ', $range ['longitude_min'] );
		$CI->db->where ( 'longitude < ', $range ['longitude_max'] );
		$query = $CI->db->get ( 'cache_location' );
		$location_rows = $query->result_array ();
		if (count ( $location_rows ) > 0) {
			$min_distance = $radius * $radius * 8;
			$nearest_location = NULL;
			foreach ( $location_rows as $location_row ) {
				$y = $location_row ['latitude'] - $latitude;
				$x = $location_row ['longitude'] - $longitude;
				$distance = $x * $x + $y * $y;
				if ($distance < $min_distance) {
					$min_distance = $distance;
					$nearest_location = $location_row;
				}
			}
			return $nearest_location;
		}
		
		// Retreive the zipcode information from the google api
		$ch = curl_init (); // initiate curl
		$key = $CI->config->config ['google_apis'] ['key'];
		$url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=$key";
		curl_setopt ( $ch, CURLOPT_URL, $url );
		curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true ); // return the output in string format
		$location_json = curl_exec ( $ch ); // execute
		if (curl_errno ( $ch )) {
			log_message ( 'error', 'Faild to call google api: ' . print_r ( curl_getinfo ( $ch ), TRUE ) );
			curl_close ( $ch ); // close curl handle
			return FALSE;
		}
		curl_close ( $ch ); // close curl handle
		
		$location_info = json_decode ( $location_json, true );
		if (! $location_info) {
			log_message ( 'error', 'Faild to parse the google api response: ' . print_r ( $location_info, TRUE ) );
			return FALSE;
		}
		
		$status = array_key_exists ( 'status', $location_info ) ? $location_info ['status'] : 'UNKNOWN';
		if ($status != "OK") {
			log_message ( 'error', "The status in the google api response is not OK: $status" );
			return FALSE;
		}
		
		// build location information
		$location_data = array (
				'latitude' => $latitude,
				'longitude' => $longitude,
				'raw_data' => $location_json 
		);
		
		$address_components = isset ( $location_info ['results'] [0] ['address_components'] ) ? $location_info ['results'] [0] ['address_components'] : NULL;
		if ($address_components) {
			$need_types = array (
					'postal_code',
					'country',
					'administrative_area_level_1',
					'administrative_area_level_2',
					'locality',
					'sublocality_level_1' 
			);
			foreach ( $address_components as $address_component ) {
				$type = $address_component ['types'] [0];
				if (in_array ( $type, $need_types )) {
					$location_data [$type] = $address_component ['long_name'];
					$location_data ["${type}_s"] = $address_component ['short_name'];
				}
			}
		}
		
		// insert the data into DB
		$CI->db->insert ( 'cache_location', $location_data );
		if ($CI->db->_error_number ())
			log_message ( 'error', 'get_loc_by_latlng: ' . $CI->db->_error_number () . ':' . $CI->db->_error_message () );
		
		return $location_data;
	}
}

if (! function_exists ( 'build_region_string_by_loc' )) {
	/**
	 *
	 * Get the region description string by location array
	 *
	 * @param array $location        	
	 * @return The string of region description
	 */
	function build_region_string_by_loc($location) {
		return $location ['locality'] . ', ' . $location ['administrative_area_level_1_s'];
	}
}

if (! function_exists ( 'calculate_latitude_longitude_range' )) {
	/**
	 *
	 * Get the range of latitude & longitude covering the circle region of the point
	 *
	 * @param float $latitude
	 *        	The latitude of the point
	 * @param float $longitude
	 *        	The longitude of the point
	 * @param float $radius
	 *        	The radius of the region
	 * @param string $unit
	 *        	The unit of radius. 'Mi' or 'Km'
	 * @return The range of latitude & longitude. latitude_min/latitude_max/longitude_min/longitude_max
	 */
	function calculate_latitude_longitude_range($latitude, $longitude, $radius, $unit = 'Mi') {
		$longitude_delta = $radius / (111.1 / cos ( deg2rad ( $latitude ) ));
		$latitude_delta = $radius / 111.1;
		if ($unit == 'Mi') {
			$longitude_delta = $longitude_delta * 1.609344;
			$latitude_delta = $latitude_delta * 1.609344;
		}
		return array (
				'longitude_min' => $longitude - $longitude_delta,
				'longitude_max' => $longitude + $longitude_delta,
				'latitude_min' => $latitude - $latitude_delta,
				'latitude_max' => $latitude + $latitude_delta 
		);
	}
}

