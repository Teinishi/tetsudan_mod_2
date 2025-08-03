local mat_rnd = matrix.multiply(
	matrix.rotationZ((math.random() - 0.5)*0.1),
	matrix.multiply(
		matrix.rotationZ((math.random() - 0.5)*0.1),
		matrix.rotationY((math.random() - 0.5)*0.1)
	)
)
local mat_mesh = matrix.identity()

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		local fv = composite.float_values
		local mat_rot = {
			fv[1], fv[2], fv[3], 0,
			fv[4], fv[5], fv[6], 0,
			fv[7], fv[8], fv[9], 0,
			0, 0, 0, 1
		}
		if composite.bool_values[1] then
			mat_mesh = matrix.multiply(mat_rnd, mat_rot)
		else
			mat_mesh = mat_rot
		end
	end
end

function onRender()
	component.renderMesh0(mat_mesh)
end
