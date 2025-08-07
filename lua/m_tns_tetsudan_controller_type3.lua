function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local smooth = true
local inserted, t = false, 0.9
local up = nil
local transform0, transform1 = matrix.identity(), matrix.identity()

function update(t_tgt)
	if inserted and math.abs(t - t_tgt) < 1e-3 then
		smooth = false
	elseif not inserted then
		smooth = true
	end
	t_tgt = (not inserted or up == nil or up > 1e-3) and 0.9 or t_tgt
	t = smooth and lerp(t, t_tgt, 0.1) or t_tgt
	local up_tgt = (not inserted and math.abs(t - 0.9) < 0.03) and 1 or 0
	up = up and clamp(up_tgt, up - 0.1, up + 0.1) or up_tgt
	local theta = lerp(90, -60, t)/180*math.pi
	transform0 = matrix.rotationY(theta)
	transform1 = matrix.multiply(transform0, matrix.translation(0, 0.1*up^2, 0))
end

function onParse()
	inserted, _ = parser.parseBool("inserted", inserted)
	t, _ = parser.parseNumber("t", t)
	update(t)
end

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		inserted = composite.bool_values[1]
		local value = composite.float_values[1]
		update(clamp(value, 0, 1))
	end
end

function onRender()
	component.renderMesh0(transform0)
	if up ~= nil and up < 0.999 then
		component.renderMesh1(transform1)
	end
end
