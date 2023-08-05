import iwidgetcasper = require('./iwidgetcasper');
/**
 * Represents a Notebook used for testing.
 */
export declare class Notebook {
    private _tester;
    private _cell_index;
    private _cells;
    private _cell_outputs;
    private _cell_outputs_errors;
    constructor(tester: iwidgetcasper.WidgetCasper);
    /**
     * Index of the last appended cell.
     */
    cell_index: number;
    /**
     * Is the notebook busy
     */
    is_busy(): boolean;
    /**
     * Is the notebook idle
     */
    is_idle(): boolean;
    /**
     * Does a cell have output
     */
    has_output(cell_index: number, output_index?: number): boolean;
    /**
     * Get the output of a cell
     */
    get_output(cell_index: number, output_index?: number): any;
    /**
     * Get the cell execution cached outputs.
     */
    get_cached_outputs(cell_index: number): any[];
    /**
     * Get the cell execution cached output errors.
     */
    get_cached_output_errors(cell_index: number): any[];
    /**
     * Check if an element exists in a cell.
     */
    cell_element_exists(cell_index: number, selector: string): boolean;
    /**
     * Utility function that allows us to execute a jQuery function
     * on an element within a cell.
     */
    cell_element_function(cell_index: string, selector: string, function_name: string, function_args: any[]): any;
    /**
     * Get the URL for the notebook server.
     */
    get_notebook_server(): string;
    /**
     * Append a cell to the notebook
     * @return cell index
     */
    append_cell(contents: string, cell_type: string): number;
    /**
     * Get an appended cell's contents.
     * @return contents
     */
    get_cell(index: number): string;
    /**
     * Execute a cell
     * @param index
     * @param expect_error - expect an error to occur when running the cell
     */
    execute_cell(index: number, expect_error?: boolean): void;
    /**
     * Opens a new notebook.
     */
    private _open_new_notebook();
    /**
     * Whether or not the page has loaded.
     */
    private _page_loaded();
    /**
     * Whether or not the kernel is running
     */
    private _kernel_running();
}
