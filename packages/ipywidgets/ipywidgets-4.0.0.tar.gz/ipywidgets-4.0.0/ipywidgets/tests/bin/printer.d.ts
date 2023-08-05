import iwidgetcasper = require('./iwidgetcasper');
import notebook = require('./notebook');
/**
 * Class that pretty prints cell information
 */
export declare class Printer {
    private _tester;
    private _notebook;
    private _printed_cells;
    constructor(tester: iwidgetcasper.WidgetCasper, notebook: notebook.Notebook);
    /**
     * Resets the printer for a new notebook.
     * Why?  The printer remembers what cells it has already
     * printed so that it never re-prints the same information.
     */
    reset(): void;
    /**
     * Pretty print a cell.
     * @param cell_index
     * @param logs - console.log logs, stored internally in WidgetCasper
     * @param logs_errors - console.error and JS error logs, stored internally in WidgetCasper
     */
    print_cell(cell_index: number, logs: string[][], logs_errors: any[][]): void;
    /**
     * Pretty print a header.
     */
    private _header(section, border_style?);
    /**
     * Pretty print body content.
     */
    private _body(section, body_style?, border_style?);
}
