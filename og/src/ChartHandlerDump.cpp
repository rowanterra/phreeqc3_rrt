// ChartHandlerDump.cpp: ChartHandler implementation for USER_GRAPH_DUMP (Mac/Linux).
// No .NET/threading; chart data is written to JSON by ChartObject.
//////////////////////////////////////////////////////////////////////
#ifdef USER_GRAPH_DUMP
#include "Phreeqc.h"
#include "ChartHandler.h"
#include <iostream>

ChartHandler::ChartHandler(PHRQ_io *io)
	: PHRQ_base(io)
{
	current_chart = NULL;
	current_chart_n_user = -1000;
	u_g_defined = false;
	timer = true;
	active_charts = 0;
}

ChartHandler::~ChartHandler()
{
	std::map<int, ChartObject *>::iterator it;
	for (it = this->chart_map.begin(); it != chart_map.end(); it++)
	{
		delete it->second;
	}
}

void
ChartHandler::Punch_user_graph(Phreeqc * phreeqc_ptr)
{
	std::map<int, ChartObject *>::iterator it = this->chart_map.begin();
	for ( ; it != chart_map.end(); it++)
	{
		if (it->second->Get_active())
		{
			this->current_chart = it->second;
			phreeqc_ptr->punch_user_graph();
		}
	}
}

bool
ChartHandler::Read(Phreeqc * phreeqc_ptr, CParser &parser)
{
	int n_user;
	std::string token;

	parser.check_line("ChartHandler", true, false, true, false);

	std::istringstream iss(parser.line());
	iss >> token;
	if (!(iss >> n_user))
	{
		n_user = 1;
	}

	std::map<int, ChartObject *>::iterator it = this->chart_map.find(n_user);
	if (it == this->chart_map.end())
	{
		chart_map[n_user] = new ChartObject(this->Get_io());
		it = this->chart_map.find(n_user);
		it->second->Set_phreeqc(phreeqc_ptr);
	}

	it->second->Read(parser);
	current_chart_n_user = n_user;
	current_chart = it->second;
	u_g_defined = true;

	if (it->second->Get_detach() && it->second->Get_form_started())
	{
		it->second->Set_end_timer(true);
		it->second->Rate_free();
	}

	if (it->second->Get_detach())
	{
		delete it->second;
		this->chart_map.erase(it);
	}
	return true;
}

bool
ChartHandler::End_timer()
{
	std::map<int, ChartObject *>::iterator it = this->chart_map.begin();
	if (chart_map.size() > 0)
	{
		screen_msg("Detaching charts...");
		if (io != NULL)
		{
			io->error_flush();
		}
	}
	for ( ; it != chart_map.end(); it++)
	{
		if (it->second->Get_form_started())
		{
			it->second->DumpChartToFile();
		}
		it->second->Rate_free();
		if (it->second->Get_form_started())
		{
			it->second->Set_end_timer(true);
			while (it->second->Get_done() != true)
			{
				/* dump path: done is set in start_chart(), so this exits immediately */
			}
		}
	}
	if (chart_map.size() > 0)
	{
		screen_msg("\rCharts detached.         \n");
		if (io != NULL)
		{
			io->error_flush();
		}
	}
	this->timer = false;
	return true;
}

bool
ChartHandler::dump(std::ostream & oss, unsigned int indent)
{
	std::map<int, ChartObject *>::iterator it = this->chart_map.begin();
	for ( ; it != chart_map.end(); it++)
	{
		it->second->dump(oss, indent);
	}
	return true;
}
#endif // USER_GRAPH_DUMP
