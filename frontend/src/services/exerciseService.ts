import apiClient from './api';
// Import shared models/types if they exist or define them here
// e.g., import { DifficultyLevel } from '../models/exercise';

// --- Interfaces based on Backend Schemas ---

// Assuming DifficultyLevel enum is defined, e.g., in models/exercise.ts
export enum DifficultyLevel {
    BEGINNER = "beginner",
    INTERMEDIATE = "intermediate",
    ADVANCED = "advanced",
}

interface Exercise {
  id: number;
  name: string;
  description?: string;
  instructions?: string;
  video_url?: string;
  image_url?: string;
  difficulty?: DifficultyLevel;
  target_body_parts?: string;
  equipment_needed?: string;
  created_by_practitioner_id?: number;
  created_at: string;
  updated_at: string;
}

interface ExerciseListResponse {
  items: Exercise[];
  total: number;
  page: number;
  page_size: number;
}

interface GetExercisesParams {
  search?: string;
  difficulty?: DifficultyLevel;
  body_part?: string;
  page?: number;
  page_size?: number;
}

// --- Program Schemas ---
// (These might live in a separate models/program.ts file)

interface ProgramExercise {
    exercise_id: number;
    order?: number;
    sets?: number;
    reps?: number;
    duration_seconds?: number;
    rest_seconds?: number;
    notes?: string;
    exercise: Exercise; // Nested Exercise details
}

interface ExerciseProgram {
    id: number;
    name: string;
    description?: string;
    created_by_practitioner_id: number;
    assigned_to_patient_id: number;
    duration_weeks?: number;
    goals?: string;
    created_at: string;
    updated_at: string;
    exercise_associations: ProgramExercise[];
}

interface ExerciseProgramListResponse {
    items: ExerciseProgram[];
    total: number;
    page: number;
    page_size: number;
}

interface GetProgramsParams {
    patient_id?: number;
    practitioner_id?: number;
    page?: number;
    page_size?: number;
}


// --- API Service Functions ---

// Function to fetch exercises
export const getExercises = async (params: GetExercisesParams): Promise<ExerciseListResponse> => {
  try {
    const response = await apiClient.get<ExerciseListResponse>('/exercises/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching exercises:', error);
    throw error;
  }
};

// Function to fetch exercise programs
export const getExercisePrograms = async (params: GetProgramsParams): Promise<ExerciseProgramListResponse> => {
    try {
        const response = await apiClient.get<ExerciseProgramListResponse>('/programs/', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching exercise programs:', error);
        throw error;
    }
};


// TODO: Add functions for other exercise/program endpoints:
// - getExerciseById(id: number): Promise<Exercise>
// - createExercise(data: ExerciseCreateData): Promise<Exercise>
// - updateExercise(id: number, data: ExerciseUpdateData): Promise<Exercise>
// - deleteExercise(id: number): Promise<void>
// - getProgramById(id: number): Promise<ExerciseProgram>
// - createProgram(data: ProgramCreateData): Promise<ExerciseProgram>
// - updateProgram(id: number, data: ProgramUpdateData): Promise<ExerciseProgram>
// - deleteProgram(id: number): Promise<void>
// - (Potentially endpoints for managing exercises within a program)
