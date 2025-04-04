import apiClient from './api';
import { AppointmentStatus } from '../models/appointment'; // Assuming models are defined elsewhere

// Define interfaces for API responses and request parameters based on backend schemas
// These might need adjustment based on the exact backend schema definitions

interface Appointment {
  id: number;
  patient_id: number;
  practitioner_id: number;
  title: string;
  start_time: string; // Assuming ISO string format
  end_time: string;   // Assuming ISO string format
  status: AppointmentStatus;
  location?: string;
  is_virtual: boolean;
  meeting_link?: string;
  patient_notes?: string;
  practitioner_notes?: string;
  created_at: string;
  updated_at: string;
  // Add other fields as needed
}

interface AppointmentListResponse {
  items: Appointment[];
  total: number;
  page: number;
  page_size: number;
}

interface GetAppointmentsParams {
  patient_id?: number;
  practitioner_id?: number;
  status?: AppointmentStatus;
  start_date?: string; // ISO string format
  end_date?: string;   // ISO string format
  page?: number;
  page_size?: number;
}

// Function to fetch appointments
export const getAppointments = async (params: GetAppointmentsParams): Promise<AppointmentListResponse> => {
  try {
    const response = await apiClient.get<AppointmentListResponse>('/appointments/', { params });
    // Convert date strings to Date objects if necessary on the frontend
    // response.data.items.forEach(item => {
    //   item.start_time = new Date(item.start_time);
    //   item.end_time = new Date(item.end_time);
    // });
    return response.data;
  } catch (error) {
    console.error('Error fetching appointments:', error);
    // Rethrow or handle error appropriately for the UI
    throw error; 
  }
};

// TODO: Add functions for other appointment endpoints:
// - getAppointmentById(id: number): Promise<Appointment>
// - createAppointment(data: AppointmentCreateData): Promise<Appointment>
// - updateAppointment(id: number, data: AppointmentUpdateData): Promise<Appointment>
// - deleteAppointment(id: number): Promise<void>
// - rescheduleAppointment(id: number, data: RescheduleData): Promise<Appointment>
// - cancelAppointment(id: number, data: CancelData): Promise<Appointment>
// - completeAppointment(id: number, data: CompleteData): Promise<Appointment>
// - getPractitionerAvailability(practitionerId: number, startDate: string, endDate: string): Promise<AvailabilityResponse>
